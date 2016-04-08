from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.db.models import signals
from django.core.exceptions import ObjectDoesNotExist


def add_default_report(sender, instance, **kwargs):
    Report.objects.get_or_create(team = instance) #this inefficiency can be removed later if there are multiple reports

class Team(models.Model):
    name = models.CharField(max_length=30)
    admin = models.ForeignKey(User, related_name='+')
    users = models.ManyToManyField(User)

    class Meta:
        unique_together = (("admin", "name"))

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.admin)


class Report(models.Model):
    team = models.ForeignKey(Team)

class Question(models.Model):
    report = models.ForeignKey(Report)
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class Survey(models.Model):
    slug = models.SlugField()
    report = models.ForeignKey(Report)
    user = models.ForeignKey(User)
    completed = models.DateTimeField(null=True, blank=True)
    date = models.DateField()


class Answer(models.Model):
    question = models.ForeignKey(Question)
    survey = models.ForeignKey(Survey)
    text = models.TextField()

signals.post_save.connect(add_default_report, sender = Team)