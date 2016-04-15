import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.utils.timezone import now

from teamreporter.models import Survey, Report, DailyReport
from teamreporter.utils import send_mass_html_mail
from teamreporterapp.celery import app

logger = logging.getLogger(__name__)


@app.task
def send_survey(survey_pk):
    survey = Survey.objects.get(pk=survey_pk)

    context = Context({'survey': survey,
                       'questions': survey.report.question_set.filter(active=True)})  # TODO: use manager instead
    context['SITE_URL'] = settings.SITE_URL
    subject = render_to_string('email/survey_subject.txt', context)

    text = get_template('email/survey.txt')
    html = get_template('email/survey.html')
    text_content = text.render(context)
    html_content = html.render(context)

    survey.user.email_user(subject, text_content, settings.DEFAULT_FROM_EMAIL, html_message=html_content)


@app.task
def generate_survey(user_pk, daily_pk):
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
    report = Report.objects.get(pk=report_pk)
    daily = report.get_daily()
    messages = []
    for user in report.team.users.all():
        context = Context({'user': user,
                           'surveys': daily.survey_set.all(),
                           'user_sent_report': daily.survey_set.filter(user=user, completed__isnull=False).exists()})
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
    for report in Report.objects.all():
        if report.can_issue_summary():
            send_summary.delay(report.pk)


@app.task
def issue_surveys():
    """
    This task is used as PeriodicTask to check which team's report should be generated and sent to all users.
    """
    survey_count = 0
    for report in Report.objects.all():
        if report.can_issue_daily():
            daily = report.get_daily()
            for user in report.team.users.all():  # TODO: take into account user roles
                if (generate_survey.delay(user.pk, daily.pk)):
                    survey_count += 1
    return survey_count
