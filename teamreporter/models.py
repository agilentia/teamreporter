from datetime import date, datetime, time
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals

from recurrence.fields import RecurrenceField
import uuid


def add_default_report(sender, instance, **kwargs):
    Report.objects.get_or_create(team=instance)  # this inefficiency can be removed later if there are multiple reports


class Team(models.Model):
    name = models.CharField(max_length=30)
    admin = models.ForeignKey(User, related_name='+')
    users = models.ManyToManyField(User, through='Membership')

    class Meta:
        unique_together = (("admin", "name"),)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.admin)


class Role(models.Model):
    name = models.CharField(max_length=30)


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now=True)
    roles = models.ManyToManyField(Role)

    class Meta:
        unique_together = (("user", "team"),)


class Report(models.Model):
    team = models.ForeignKey(Team)
    recurrences = RecurrenceField(null=True)
    send_time = models.TimeField(default=time(10, 0))
    summary_time = models.TimeField(default=time(18, 0))

    # This variable is used in order to ensure summary is not sent twice a day
    summary_submitted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{0} - {1}'.format(self.pk, self.team)

    @property
    def occurs_today(self):
        """
        Returns True if report should be submitted today.
        """
        if not self.recurrences:
            return False
        today = date.today()
        today = datetime.combine(today, datetime.min.time())
        return self.recurrences.after(today, inc=True).date() == date.today()


class Question(models.Model):
    report = models.ForeignKey(Report)
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class Survey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(Report)
    user = models.ForeignKey(User)
    completed = models.DateTimeField(null=True, blank=True)
    date = models.DateField()


class Answer(models.Model):
    question = models.ForeignKey(Question)
    survey = models.ForeignKey(Survey)
    text = models.TextField()

    class Meta:
        unique_together = ('survey', 'question')


signals.post_save.connect(add_default_report, sender=Team)
