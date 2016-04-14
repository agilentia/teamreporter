from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import SurveyForm
from .models import Team, User, Question, Role, Membership, Report, Survey, Answer, DailyReport
from .decorators import survey_completed
import recurrence
import datetime
import json
import dateutil.parser


def check_scope(request, team):
    if team.admin.email != request.user.email:
        raise Http404("Team doesn't exist")


def validate_presence(d, keys):
    for k in keys:
        if k not in d:
            return False
    return True


def clean(d, keys):
    """only allow whitelisted keys"""
    return {k: v for k, v in d.items() if k in keys}


@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class TeamView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        return JsonResponse({"teams": [model_to_dict(t, exclude=["users"]) for t in Team.objects.filter(admin=user)]})

    def post(self, request, *args, **kwargs):
        user = request.user
        team_info = json.loads(request.body.decode("utf-8"))

        if not validate_presence(team_info, ["name", "days_of_week", "survey_send_time", "summary_send_time"]):
            return JsonResponse({"error": "Invalid Team JSON data"}, status=400)

        survey_send_time = dateutil.parser.parse(team_info["survey_send_time"]).replace(second=0, microsecond=0)
        summary_send_time = dateutil.parser.parse(team_info["summary_send_time"]).replace(second=0, microsecond=0)
        rule = recurrence.Rule(recurrence.WEEKLY, byday=team_info["days_of_week"])
        rec = recurrence.Recurrence(rrules=[rule])

        cleaned_team_info = clean(team_info, ["name"])
        try:
            team = Team.objects.create(admin=user, **cleaned_team_info)
        except ValidationError:
            return JsonResponse({"error": "Team already exists with this name"},
                                status=400)  # should also check error code to ensure its violating the unique together constraint (likely is)

        Report.objects.create(team=team, recurrences=rec, survey_send_time=survey_send_time,
                              summary_send_time=summary_send_time)
        return JsonResponse({"team": model_to_dict(team)})

    def delete(self, request, *args, **kwargs):
        pass


@method_decorator(login_required, name='dispatch')
class UserView(View):
    def get(self, request, *args, **kwargs):
        team_id = int(self.kwargs["team_id"])
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)
        memberships = team.membership_set.all()
        users = []
        for m in memberships:  # TODO: make this little loop a method call on the object manager
            user_info = model_to_dict(m.user, fields=["email", "first_name", "last_name", "id"])
            user_info["roles"] = [model_to_dict(r) for r in m.roles.all()]
            users.append(user_info)

        return JsonResponse({"users": users})

    def post(self, request, *args, **kwargs):
        team_id = int(self.kwargs["team_id"])
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)

        user_info = json.loads(request.body.decode("utf-8"))
        if not validate_presence(user_info, ["email", "roles"]):
            return JsonResponse({"error": "Invalid User JSON data"}, status=400)

        cleaned_user_info = clean(user_info, ["first_name", "last_name", "email", ])
        role_ids = [role["id"] for role in user_info["roles"]]
        try:
            user = User.objects.get(email=cleaned_user_info["email"])
        except ObjectDoesNotExist:
            user = User.objects.create(username=cleaned_user_info["email"], **cleaned_user_info)

        try:
            membership = Membership.objects.create(team=team, user=user)
            membership.roles.add(*role_ids)
            membership.save()
        except IntegrityError:
            JsonResponse({"error": "User already a part of team"}, status=400)
        user_dict = model_to_dict(user, fields=['email', 'first_name', 'last_name', 'id'])
        user_dict["roles"] = user_info["roles"]
        return JsonResponse({"user": user_dict})

    def delete(self, request, *args, **kwargs):
        user_id = int(self.kwargs["user_id"])
        team_id = int(self.kwargs["team_id"])
        user = get_object_or_404(User, pk=user_id)
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)
        Membership.objects.filter(user=user, team=team).delete()

        return JsonResponse({"user": model_to_dict(user, fields=("email", "id"))})


@method_decorator(login_required, name='dispatch')
class ReportView(View):
    def get(self, request, *args, **kwargs):
        team_id = int(self.kwargs["team_id"])
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)
        report = team.report_set.first()
        questions = report.question_set.filter(active=True)

        return JsonResponse({"questions": [model_to_dict(q) for q in questions]})

    def post(self, request, *args, **kwargs):
        team_id = int(self.kwargs["team_id"])
        team = get_object_or_404(Team, pk=team_id)
        check_scope(request, team)

        report_info = json.loads(request.body.decode("utf-8"))
        validate_presence(report_info, ["question"])
        question_string = report_info["question"]
        question = Question.objects.create(text=question_string, report=team.report_set.first())

        return JsonResponse({"question": model_to_dict(question)})

    def delete(self, request, *args, **kwargs):
        question_id = int(self.kwargs["question_id"])
        question = get_object_or_404(Question, pk=question_id)
        team = question.report.team
        check_scope(request, team)

        question.active = False
        question.save()

        return JsonResponse({"question": model_to_dict(question, fields=("text", "id"))})


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
        kwargs['questions'] = self.survey.report.question_set.filter(active=True)
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


class ThankYouView(TemplateView):
    template_name = 'thankyou.html'


@method_decorator(login_required, name='dispatch')
class RoleView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"roles": [model_to_dict(r, fields=["id", "name"]) for r in Role.objects.all()]})


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
        context['questions'] = survey.report.question_set.filter(active=True)
        return context
