from django.test import TestCase
from datetime import time, datetime

from .models import Report, User, Team, Membership, Question
import recurrence


class TestNegativeReport(TestCase):
    def setUp(self):
        all_days_but_today = list(range(7))
        all_days_but_today.remove(datetime.today().weekday())
        rule_not = recurrence.Rule(recurrence.WEEKLY, byday=all_days_but_today)
        rec_not = recurrence.Recurrence(rrules=[rule_not])
        self.admin = User.objects.create(email="celery@admin.com", username="celery_admin")
        self.team = Team.objects.create(name="celery_team_test", admin=self.admin)
        self.report_not_today = Report.objects.create(team=self.team, recurrences=rec_not, survey_send_time=time.min)
        self.report = Report.objects.create(team=self.team, survey_send_time=time.min,
                                            recurrences=recurrence.Recurrence(rrules=[recurrence.Rule(recurrence.WEEKLY,
                                                                                                      byday=range(7))]))

    def test_not_occurs_today(self):
        self.assertFalse(self.report_not_today.occurs_today)

    def test_report_without_questions(self):
        self.assertTrue(self.report.occurs_today)
        self.assertFalse(self.report.can_issue_daily())


class TestReport(TestCase):
    def setUp(self):
        rule = recurrence.Rule(recurrence.WEEKLY, byday=range(7))
        rec = recurrence.Recurrence(rrules=[rule])
        self.admin = User.objects.create(email="celery@admin.com", username="celery_admin")
        self.team = Team.objects.create(name="celery_team_test", admin=self.admin)
        self.membership = Membership.objects.create(team=self.team, user=self.admin)
        self.report = Report.objects.create(team=self.team, recurrences=rec, survey_send_time=time.min)
        self.question = Question.objects.create(report=self.report, text='test')

    def test_occurs_today(self):
        """
        Tests occurs_today property
        Decides whether or not a daily report should be created for today
        """

        self.assertTrue(self.report.occurs_today)

    def test_can_issue_daily(self):
        """
        Tests can_issue_daily method
        Decides if the daily report surveys can be sent out or not
        """

        self.assertTrue(self.report.can_issue_daily())  # if daily report isn't issued, should be True
        self.report.survey_send_time = time.max
        self.assertFalse(self.report.can_issue_daily())  # if hour is later than current time, don't issue
        self.report.survey_send_time = time.min
        self.report.get_daily()  # create daily report
        self.assertFalse(self.report.can_issue_daily(),
                         "Assumed after daily report is created the daily report has already been sent")

    def test_get_daily(self):
        """
        Tests get_daily method
        Grabs the report instance for a particular day.  Unique for day/report
        """

        first = self.report.get_daily()
        second = self.report.get_daily()
        self.assertTrue(
            first == second)  # ensures the same daily report was grabbed from the DB and a new one wasn't created
        self.assertTrue(second)  # just ensures its not returning None

    def test_can_issue_summary(self):
        """
        Tests can_issue_summary
        Decides if summary for daily report can be sent out or not based on if it already has and if the daily report has been created
        """

        daily = self.report.get_daily()
        daily.delete()
        self.assertFalse(self.report.can_issue_summary(),
                         "Daily report hasn't been created yet, summary should not be submitted")
        daily = self.report.get_daily()

        self.report.summary_send_time = time.min
        self.assertTrue(self.report.can_issue_summary(),
                        "Daily report created but summary hasn't been submitted.  Should be allowed")

        daily.summary_submitted = datetime.now()
        daily.save()
        self.assertFalse(self.report.can_issue_summary(),
                         "Daily report created and summary been submitted.  No more summaries should be allowed")
