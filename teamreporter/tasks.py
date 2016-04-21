from django.conf import settings
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.utils.timezone import now

from teamreporter.models import Survey, Report, DailyReport
from teamreporter.utils import send_mass_html_mail
from teamreporterapp.celery import app

import logging

logger = logging.getLogger(__name__)


@app.task
def send_survey(survey_pk):
    """
    Emails a team's questions to the survey's (id=survey_pk) its corresponding contributor

    :param survey_pk: Survey's primary key value
    :return: Nothing
    :rtype: None
    """
    survey = Survey.objects.get(pk=survey_pk)

    context = Context({'survey': survey,
                       'questions': survey.report.question_set.active()})
    context['SITE_URL'] = settings.SITE_URL
    subject = render_to_string('email/survey_subject.txt', context)

    text = get_template('email/survey.txt')
    html = get_template('email/survey.html')
    text_content = text.render(context)
    html_content = html.render(context)

    survey.user.email_user(subject, text_content, settings.DEFAULT_FROM_EMAIL, html_message=html_content)


@app.task
def generate_survey(user_pk, daily_pk):
    """
    Creates a survey for a contributor on a team using the team's report's current questions

    :param user_pk: User's primary key value
    :param daily_pk: Daily report's primary key value
    :return: True if survey created, False/None otherwise
    :rtype: bool
    """
    user = User.objects.get(pk=user_pk)
    daily = DailyReport.objects.get(pk=daily_pk)
    if not daily.report.team.users.filter(pk=user_pk).exists():
        logger.warning('Generate survey executed with user from outside team!')
        return False

    survey, created = Survey.objects.get_or_create(user=user, daily=daily)
    if created:
        # prepare email and send it to user
        logger.info('Sending survey to team member')
        send_survey.delay(survey.pk)
        return True


@app.task
def send_summary(report_pk):
    """
    Sends all surveys filled out by contributors for the id=report_pk's daily report to the stakeholders

    :param report_pk: Report's primary key value
    :return: Nothing
    :rtype: None
    """
    report = Report.objects.get(pk=report_pk)
    daily = report.get_daily()
    messages = []
    questions = daily.report.question_set.active()
    surveys = daily.survey_set.all()
    for user in report.stakeholders:
        context = Context({'user': user,
                           'daily': daily,
                           'surveys': surveys,
                           'questions': questions})
        context['SITE_URL'] = settings.SITE_URL
        subject = render_to_string('email/summary_subject.txt', context)

        text = get_template('email/summary.txt')
        html = get_template('email/summary.html')
        text_content = text.render(context)
        html_content = html.render(context)
        messages.append([subject, text_content, html_content, settings.DEFAULT_FROM_EMAIL, [user.email]])

    send_mass_html_mail(messages)
    daily.summary_submitted = now()
    daily.save()


@app.task
def issue_summaries():
    """
    Sends out all daily report summaries to its stakeholders that should be sent out at the current time on the current day

    :return: Nothing
    :rtype: None
    """
    for report in (r for r in Report.objects.all() if r.can_issue_summary()):
        send_summary.delay(report.pk)


@app.task
def issue_surveys():
    """
    Sends out all daily surveys to its contributors that should be sent out at the current time on the current day

    :return: Total number of surveys sent out
    :rtype: int
    """
    survey_count = 0
    for report in (r for r in Report.objects.all() if r.can_issue_daily()):
        daily = report.get_daily()
        for user in report.contributors:
            if generate_survey.delay(user.pk, daily.pk):
                survey_count += 1
    return survey_count
