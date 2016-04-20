from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

from cerberus import Validator
from dateutil import parser

from .enums import DAYS
from .forms import SurveyForm
from .models import Team, User, Question, Role, Membership, Report, Survey, Answer, DailyReport
from .validators import team_schema, user_schema, question_schema
from .decorators import survey_completed

import recurrence
import json
import hashlib

import logging

logger = logging.getLogger(__name__)


def check_scope(request, team):
    if team.admin != request.user:
        raise Http404("Team doesn't exist")


@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class TeamView(View):
    def report_dict(self, team):
        report = team.report_set.first()
        days = [DAYS.index(day_string) for day_string in report.recurrences.rrules[0].byday]
        report_dict = model_to_dict(report, exclude=['recurrences'])
        report_dict['days_of_week'] = days

        return report_dict

    def get(self, request, *args, **kwargs):
        user = request.user
        teams = []
        for team in Team.objects.filter(admin=user):
            team_dict = model_to_dict(team, exclude=['users'])
            team_dict['report'] = self.report_dict(team)
            teams.append(team_dict)
        return JsonResponse({'teams': teams})

    def post(self, request, *args, **kwargs):
        user = request.user
        team_info = json.loads(request.body.decode("utf-8"))
        validator = Validator(team_schema)
        if not validator.validate(team_info):
            return JsonResponse({'error': validator.errors})
        survey_send_time = parser.parse(team_info['send_time']).replace(second=0, microsecond=0)
        summary_send_time = parser.parse(team_info['summary_time']).replace(second=0, microsecond=0)
        rule = recurrence.Rule(recurrence.WEEKLY, byday=team_info['days_of_week'])
        rec = recurrence.Recurrence(rrules=[rule])

        try:
            team = Team.objects.create(admin=user, name=team_info['name'])
        except IntegrityError:
            return JsonResponse({'error': {"name": _("team with this name already exists")}})
        Report.objects.create(team=team, recurrences=rec, survey_send_time=survey_send_time,
                              summary_send_time=summary_send_time)
        team_dict = model_to_dict(team, exclude=['users'])
        team_dict['report'] = self.report_dict(team)
        return JsonResponse({'team': team_dict})

    def put(self, request, *args, **kwargs):
        team_info = json.loads(request.body.decode('utf-8'))

        validator = Validator(team_schema)
        if not validator.validate(team_info):
            return JsonResponse({'error': validator.errors})

        try:
            team = Team.objects.get(id=int(self.kwargs['team_id']))
        except ObjectDoesNotExist:
            return JsonResponse({'error': [{"Team ID": "Team not found for ID in request"}]})

        check_scope(request, team)

        report = team.report_set.first()
        if 'send_time' in team_info:
            report.survey_send_time = parser.parse(team_info['send_time']).replace(second=0, microsecond=0)
        if 'summary_time' in team_info:
            report.summary_send_time = parser.parse(team_info['summary_time']).replace(second=0, microsecond=0)
        if 'days_of_week' in team_info:
            rule = recurrence.Rule(recurrence.WEEKLY, byday=team_info['days_of_week'])
            rec = recurrence.Recurrence(rrules=[rule])
            report.recurrences = rec
        if 'name' in team_info:
            team.name = team_info['name']
        report.save()

        try:
            team.save()
        except IntegrityError:
            return JsonResponse({'error': {"name": _("team with this name already exists")}})

        team_dict = model_to_dict(team, exclude=['users'])
        team_dict['report'] = self.report_dict(team)
        return JsonResponse({'team': team_dict})

    def delete(self, request, *args, **kwargs):
        team_id = int(self.kwargs['team_id'])
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)
        team.delete()
        team_dict = {'id': team_id}
        return JsonResponse({'team': team_dict})


@method_decorator(login_required, name='dispatch')
class UserView(View):
    def get(self, request, *args, **kwargs):
        team_id = int(self.kwargs['team_id'])
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)
        memberships = team.membership_set.all()
        users = []
        for m in memberships:  # TODO: make this little loop a method call on the object manager
            user_info = model_to_dict(m.user, fields=['email', 'first_name', 'last_name', 'id'])
            user_info['roles'] = [model_to_dict(r) for r in m.roles.all()]
            users.append(user_info)

        return JsonResponse({'users': users})

    def post(self, request, *args, **kwargs):
        team_id = int(self.kwargs['team_id'])
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)

        user_info = json.loads(request.body.decode('utf-8'))
        validator = Validator(user_schema)
        if not validator.validate(user_info):
            return JsonResponse({'error': validator.errors})

        role_ids = [role['id'] for role in user_info['roles']]
        defaults = {k: user_info[k] for k in ['first_name', 'last_name', 'email']}
        defaults['username'] = hashlib.md5(user_info['email'].encode('utf-8')).hexdigest()[:30]
        user, created = User.objects.get_or_create(email=user_info['email'], defaults=defaults)

        try:
            membership = Membership.objects.create(team=team, user=user)
            membership.roles.add(*role_ids)
            membership.save()
        except IntegrityError:
            return JsonResponse({'error': {"name": _("user already part of the team")}})
        user_dict = model_to_dict(user, fields=['email', 'first_name', 'last_name', 'id'])
        user_dict['roles'] = user_info['roles']
        return JsonResponse({'user': user_dict})

    def delete(self, request, *args, **kwargs):
        user_id = int(self.kwargs['user_id'])
        team_id = int(self.kwargs['team_id'])
        user = get_object_or_404(User, pk=user_id)
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)
        Membership.objects.filter(user=user, team=team).delete()

        return JsonResponse({'user': model_to_dict(user, fields=('email', 'id'))})


@method_decorator(login_required, name='dispatch')
class QuestionView(View):
    def get(self, request, *args, **kwargs):
        team_id = int(self.kwargs['team_id'])
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)
        report = team.report_set.first()
        questions = report.question_set.active()

        return JsonResponse({'questions': [model_to_dict(q, fields=['id', 'text']) for q in questions]})

    def put(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'], report__team=self.kwargs['team_id'])
        team = question.report.team
        check_scope(request, team)
        info = json.loads(request.body.decode('utf-8'))

        validator = Validator(question_schema)
        if not validator.validate(info):
            return JsonResponse({'error': validator.errors})

        new_question = Question.objects.create(text=info['question'], report=question.report)
        question.active = False
        question.save()
        return JsonResponse({'question': model_to_dict(new_question, fields=('text', 'id'))})

    def post(self, request, *args, **kwargs):
        team_id = int(self.kwargs['team_id'])
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)
        report_info = json.loads(request.body.decode('utf-8'))

        validator = Validator(question_schema)
        if not validator.validate(report_info):
            return JsonResponse({'error': validator.errors})

        question_string = report_info['question']
        question = Question.objects.create(text=question_string, report=team.report_set.first())
        return JsonResponse({'question': model_to_dict(question, fields=('text', 'id'))})

    def delete(self, request, *args, **kwargs):
        question_id = int(self.kwargs['question_id'])
        question = get_object_or_404(Question, pk=question_id)
        team = question.report.team
        check_scope(request, team)

        question.active = False
        question.save()

        return JsonResponse({'question': model_to_dict(question, fields=('text', 'id'))})


@method_decorator(survey_completed, 'dispatch')
class SurveyView(FormView):
    template_name = 'survey.html'
    form_class = SurveyForm
    success_url = '/thankyou/'

    @property
    def survey(self):
        return get_object_or_404(Survey, pk=self.kwargs['uuid'])

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form. Include ``questions`` for initiating survey.
        """
        kwargs = super(SurveyView, self).get_form_kwargs()
        kwargs['questions'] = self.survey.report.question_set.active()
        return kwargs

    def form_valid(self, form):
        survey = self.survey
        for question_pk, response in form.extract_answers():
            question = Question.objects.get(pk=question_pk)
            answer, created = Answer.objects.get_or_create(question=question, survey=survey)
            answer.text = response
            answer.save()

        survey.completed = now()
        survey.save()

        return super(SurveyView, self).form_valid(form)


class GenericErrorPage(TemplateView):
    template_name = "errors/generic.html"
    code = None
    description = None
    title = None

    def get_context_data(self, **kwargs):
        context = super(GenericErrorPage, self).get_context_data(**kwargs)
        context['code'] = self.code
        context['description'] = self.description
        context['title'] = self.title
        return context


class ThankYouView(TemplateView):
    template_name = 'thankyou.html'


@method_decorator(login_required, name='dispatch')
class RoleView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'roles': [model_to_dict(r, fields=['id', 'name']) for r in Role.objects.all()]})


@method_decorator(staff_member_required, name='dispatch')
class SummaryDebugPreview(TemplateView):
    template_name = 'email/summary.html'

    def get_context_data(self, **kwargs):
        context = super(SummaryDebugPreview, self).get_context_data(**kwargs)
        daily = get_object_or_404(DailyReport, pk=kwargs['report'])
        context.update({'user': self.request.user,
                        'surveys': daily.survey_set.all(),
                        'user_sent_report': daily.survey_set.filter(user=self.request.user,
                                                                    completed__isnull=False).exists()})
        return context


@method_decorator(staff_member_required, name='dispatch')
class SurveyDebugPreview(TemplateView):
    template_name = 'email/survey.html'

    def get_context_data(self, **kwargs):
        context = super(SurveyDebugPreview, self).get_context_data(**kwargs)
        survey = Survey.objects.get(pk=kwargs['survey'])
        context['survey'] = survey
        context['questions'] = survey.report.question_set.active()
        return context
