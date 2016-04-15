from .tasks import send_survey, generate_survey, send_summary, issue_summaries, issue_surveys
from unittest.mock import MagicMock
from django.test.utils import override_settings
from django.test import Client, TestCase
from .models import Report, Team, Membership, User, Survey, Role
import recurrence
from datetime import time

class TestTasks(TestCase):
    fixtures = ["teamreporter/fixtures/roles.json"]

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')

    def setUp(self):
        rule = recurrence.Rule(recurrence.WEEKLY, byday = list(range(7)))
        rec = recurrence.Recurrence(rrules = [rule])
        self.admin = User.objects.create(email="celery@admin.com", username="celery_admin")
        self.user = User.objects.create(email="celery@user.com", username="celery_user")
        self.team = Team.objects.create(name = "celery_team_test", admin=self.admin)
        roles = Role.objects.all()
        self.membership = Membership.objects.create(user=self.user, team = self.team)
        for r in roles:
            self.membership.roles.add(r)

        self.team.membership_set.add(self.membership)
        self.report = Report.objects.create(team = self.team, recurrences = rec, survey_send_time=time(0, 0))
        self.report.can_issue_daily = MagicMock(return_value = True)

    def test_generate_survey(self):
        """
        tests survey generation
        Survey should be created if daily report exists/is valid and the user the survey is going to is actually on the team
        """

        result = generate_survey(self.user.id, self.report.get_daily()).get()  # should create a survey given a valid daily report and user on the team
        self.assertTrue(result)

        result = generate_survey(3, self.report.get_daily()).get()  # User is not on this team therefore survey shouldn't be created
        self.assertFalse(result)

    def test_issue_survey(self):
        """
        Test survey issuing
        TODO: test multiple users

        Returns the number of users a survey was sent to.  TODO: issue_survey can probably return something with more info in the future
        """
        result = issue_surveys.apply().get()
        self.assertTrue(result == 1)
        self.membership.roles.filter(name="contributor").delete()
        self.report.get_daily().delete()  # 'reset' daily report
        result = issue_surveys.apply().get()
        self.assertTrue(result == 0) #should be sent to contributors only only!!

    def test_send_survey(self):
        pass

    def test_send_summary(self):
        pass

    def test_issue_summaries(self):
        pass

