from datetime import date, datetime, time
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from recurrence.fields import RecurrenceField
import uuid


class Team(models.Model):
    name = models.CharField(max_length=30)
    admin = models.ForeignKey(User, related_name='+')
    users = models.ManyToManyField(User, through='Membership')

    class Meta:
        unique_together = ('admin', 'name')

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.admin)


class Role(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now=True)
    roles = models.ManyToManyField(Role)

    class Meta:
        unique_together = ('user', 'team')


class Report(models.Model):
    team = models.ForeignKey(Team)
    recurrences = RecurrenceField(null=True)
    survey_send_time = models.TimeField(default=time(10, 0))
    summary_send_time = models.TimeField(default=time(18, 0))

    def __str__(self):
        return 'Report ({0}) from {1} flow {2}=>{3}'.format(self.pk, self.team, self.survey_send_time,
                                                            self.summary_send_time)

    def has_contributor(self, user):
        return self.team.users.filter(membership__roles__name='contributor', membership__user=user)

    def has_stakeholder(self, user):
        return self.team.users.filter(membership__roles__name='stakeholder', membership__user=user)

    def can_issue_daily(self):
        """
        ``Report`` can issue ``DailyReport`` if and only if
            - occurs today ( hence ``get_daily`` ),
            - daily hasn't been issued yet for day.
        """
        already_issued = self.dailyreport_set.filter(date=date.today()).exists()
        return self.occurs_today and self.survey_send_time <= now().time() and not already_issued

    def can_issue_summary(self):
        if self.dailyreport_set.filter(date=date.today()).exists():
            return self.get_daily().summary_submitted is None
        return False

    def get_daily(self):
        """
        Return ``DailyReport`` tailored for current day. Skip created part entirely.
        """
        return DailyReport.objects.get_or_create(report=self)[0]

    @property
    def occurs_today(self):
        """
        Returns True if recurrences contain current date.
        """
        if not self.recurrences:
            return False

        today = date.today()
        today = datetime.combine(today, datetime.min.time())
        return self.recurrences.after(today, inc=True).date() == date.today()


class DailyReport(models.Model):
    report = models.ForeignKey(Report)
    date = models.DateField(default=date.today)
    summary_submitted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'Daily ({0}) from {1}'.format(self.pk, self.report.team)

    class Meta:
        unique_together = ('report', 'date')


class Question(models.Model):
    report = models.ForeignKey(Report)
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Question {0} from Report {1}'.format(self.pk, self.report.pk)


class Survey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    daily = models.ForeignKey(DailyReport)
    user = models.ForeignKey(User)
    completed = models.DateTimeField(null=True, blank=True)

    @property
    def report(self):
        return self.daily.report

    def __str__(self):
        return "Survey for {0} on {1}".format(self.user, self.daily)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    survey = models.ForeignKey(Survey)
    text = models.TextField()

    class Meta:
        unique_together = ('survey', 'question')
