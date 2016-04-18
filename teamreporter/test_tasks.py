from django.core import mail
from django.test.utils import override_settings
from django.test import TestCase
from django.utils.timezone import now

from .tasks import generate_survey, issue_surveys, issue_summaries
from .models import Report, Team, Membership, User, Role, Survey

from datetime import time
from unittest import mock

import recurrence


class TestTasks(TestCase):
    fixtures = ['teamreporter/fixtures/roles.json']

    def setUp(self):
        rule = recurrence.Rule(recurrence.WEEKLY, byday=list(range(7)))
        rec = recurrence.Recurrence(rrules=[rule])
        self.admin = User.objects.create(email='celery@admin.com', username='celery_admin')
        self.user = User.objects.create(email='celery@user.com', username='celery_user')
        self.team = Team.objects.create(name='celery_team_test', admin=self.admin)
        roles = Role.objects.all()
        self.membership = Membership.objects.create(user=self.user, team=self.team)
        for r in roles:
            self.membership.roles.add(r)

        self.team.membership_set.add(self.membership)
        self.report = Report.objects.create(team=self.team, recurrences=rec, summary_send_time=time.max,
                                            survey_send_time=time.max)

    @override_settings(CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_generate_survey(self):
        """
        tests survey generation
        Survey should be created if daily report exists/is valid and the user the survey is going to is actually on the team
        """

        result = generate_survey.apply((self.user.id,
                                        self.report.get_daily().id)).get()
        self.assertTrue(result, "should create a survey given a valid daily report and user on the team")

        result = generate_survey.apply((self.admin.id,
                                        self.report.get_daily().id)).get()
        self.assertFalse(result, "User is not on this team therefore survey shouldn't be created")

    @override_settings(CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_issue_survey(self):
        """
        Test survey issuing
        TODO: test multiple users

        Returns the number of users a survey was sent to.  TODO: issue_survey can probably return something with more info in the future
        """

        with mock.patch.object(Report, 'can_issue_daily', return_value=True):
            result = issue_surveys.apply().get()
        self.assertEqual(result, 1, 'task should generate at least one survey')
        self.assertEquals(len(mail.outbox), 1, 'there should be nice email sent to user')

        message = mail.outbox[0]
        html_body = message.alternatives[0][0]
        self.assertIn('Boomerang calling in', message.subject, 'title contains positive message')
        self.assertIn(str(Survey.objects.get().pk), message.body, 'body  contains link with survey pk')
        self.assertIn(str(Survey.objects.get().pk), html_body, 'also html body')

    @override_settings(CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_issue_survey_not_contributor(self):
        self.membership.roles.filter(name='contributor').delete()
        self.report.get_daily().delete()  # 'reset' daily report
        result = issue_surveys.apply().get()
        self.assertEqual(result, 0, 'should be sent to contributors only only!!')

    @override_settings(CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_invalid_issue_survey_conditions(self):
        with mock.patch.object(Report, 'can_issue_daily', return_value=False) as cid_mock:
            result = issue_surveys.apply().get()
            cid_mock.assert_called_with()

        self.assertEqual(result, 0, "can't issue survey without can_issue_daily permission")

    @override_settings(CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_issue_summaries(self):
        with mock.patch.object(Report, 'can_issue_daily', return_value=True):
            result = issue_surveys.apply().get()
        self.assertEqual(result, 1, 'task should generate at least one survey')
        survey = Survey.objects.get()
        survey.completed = now()

        with mock.patch.object(Report, 'can_issue_summary', return_value=True):
            issue_summaries.apply()
        self.assertEquals(len(mail.outbox), 2, 'there should be two emails sent to user')

        self.assertIsNotNone(Report.objects.get().dailyreport_set.get().summary_submitted)
        message = mail.outbox[1]
        self.assertIn('Boomerang summary report', message.subject, 'title contains positive message')
