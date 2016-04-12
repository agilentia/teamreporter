import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.utils.timezone import now

from teamreporter.models import Survey, Report
from teamreporter.utils import send_mass_html_mail
from teamreporterapp.celery import app

logger = logging.getLogger(__name__)


@app.task
def send_survey(survey_pk):
    survey = Survey.objects.get(pk=survey_pk)

    context = Context({'user': survey.user, 'survey': survey,
                       'questions': survey.report.question_set.filter(active=True)})  # TODO: use manager instead
    subject = render_to_string('email/survey_subject.txt', context)

    text = get_template('email/survey.txt')
    html = get_template('email/survey.html')
    text_content = text.render(context)
    html_content = html.render(context)

    survey.user.email_user(subject, text_content, settings.DEFAULT_FROM_EMAIL, html_message=html_content)


@app.task
def generate_survey(user_pk, report_pk):
    user = User.objects.get(pk=user_pk)
    report = Report.objects.get(pk=report_pk)

    if user not in report.team.users:
        logger.warning('Generate survey executed with user from outside team!')
        return False

    survey, created = Survey.objects.get_or_create(user=user, report=report, date=now().date())

    if created:
        # prepare email and send it to user
        logger.info('Sending survey to team member')
        send_survey.delay(survey.pk)
        return True


@app.task
def send_summary(report_pk):
    report = Report.objects.get(pk=report_pk)
    messages = []
    for user in report.team.users.all():
        context = Context({'user': user, 'surveys': report.survey_set.all(),
                           'user_sent_report': Survey.objects.get(report=report, user=user).completed is not None})
        subject = render_to_string('email/summary_subject.txt', context)

        text = get_template('email/summary.txt')
        html = get_template('email/summary.html')
        text_content = text.render(context)
        html_content = html.render(context)
        messages.append([subject, text_content, html_content, settings.DEFAULT_FROM_EMAIL, [user.email]])

    send_mass_html_mail(messages)
    report.summary_submitted = now()
    report.save()


@app.task
def issue_summaries():
    for report in Report.objects.all():
        if report.occurs_today and report.summary_time <= now().time() and not report.summary_submitted:
            send_summary.delay(report.pk)


@app.task
def issue_surveys():
    """
    This task is used as PeriodicTask to check hourly which team's report should be generated and sent to all users.
    """

    for report in Report.objects.all():
        if report.occurs_today and report.send_time <= now().time():
            # TODO: double check if there's no surveys generated for any team member given day
            for user in report.team.users:
                generate_survey.delay(user.pk, report.pk)
