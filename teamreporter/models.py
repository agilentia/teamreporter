from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.db.models import signals
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json

def validate_roles(role_string):
    roles = json.loads(role_string)
    print("COUNT", Role.objects.filter(id__in=roles).count())
    if Role.objects.filter(id__in=roles).count() != len(roles):
        raise ValidationError("Not all role IDs were found")


def add_default_report(sender, instance, **kwargs):
    Report.objects.get_or_create(team=instance)  # this inefficiency can be removed later if there are multiple reports

class Team(models.Model):
    name = models.CharField(max_length=30)
    admin = models.ForeignKey(User, related_name='+')
    users = models.ManyToManyField(User, through = 'Membership')

    class Meta:
        unique_together = ("admin", "name")

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.admin)

class Role(models.Model):
    name = models.CharField(max_length = 30)

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now=True)
    roles = models.CharField(max_length = 50, validators = [validate_roles,])

    def set_roles(self, roles):
        self.roles = json.dumps(roles)

    def get_roles(self, roles):
        return json.loads(self.roles)

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


signals.post_save.connect(add_default_report, sender=Team)
