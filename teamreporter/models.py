from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=30)
    admin = models.ForeignKey(User, related_name='+')
    users = models.ManyToManyField(User)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.admin)


class Question(models.Model):
    group = models.ForeignKey(Group)
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class Survey(models.Model):
    slug = models.SlugField()
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    questions = models.ManyToManyField(Question)
    completed = models.DateTimeField(null=True, blank=True)
    date = models.DateField()


class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    survey = models.ForeignKey(Survey)
    text = models.TextField()
