from django.conf import settings
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.utils.timezone import now

from teamreporter.models import Survey, Report
from teamreporterapp.celery import app


@app.task
def generate_survey(user_pk, report_pk):
    user = User.objects.get(pk=user_pk)
    report = Report.objects.get(pk=report_pk)

    survey, created = Survey.objects.get_or_create({
        'user': user,
        'report': report,
        'date': now().date()
    })

    if created:
        # prepare email and send it to user

        context = Context({'user': user, 'questions': report.question_set.filter(active=True)})
        subject = render_to_string('email/survey_subject.txt', context)

        text = get_template('email/survey.txt')
        html = get_template('email/survey.html')
        text_content = text.render(context)
        html_content = html.render(context)

        user.email_user(subject, text_content, settings.DEFAULT_FROM_EMAIL, html_message=html_content)



@app.task
def issue_surveys():
    """
    This task is used as PeriodicTask to check hourly which team's report should be generated and sent to all users.
    """

    for report in Report.objects.all():
        if report.occurs_today and report.time <= now().time():
            # TODO: double check if there's no surveys generated for any team member given day
            for user in report.team.users:
                generate_survey.delay(user.pk, report.pk)
