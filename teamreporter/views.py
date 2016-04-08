from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Team, User, Question
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json


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
        if not validate_presence(team_info, ["name"]):
            return JsonResponse({"error": "Invalid Team JSON data"}, status=400)
        cleaned_team_info = clean(team_info, ["name"])
        try:
            team = Team.objects.create(admin=user, **cleaned_team_info)
        except ValidationError:
            return JsonResponse({"error": "Team already exists with this name"},
                                status=400)  # should also check error code to ensure its violating the unique together constraint (likely is)

        return JsonResponse({"team": model_to_dict(team)})

    def delete(self, request, *args, **kwargs):
        pass


@method_decorator(login_required, name='dispatch')
class UserView(View):
    def check_scope(self, request, team):
        if team.admin.email != request.user.email:
            raise Http404("Team doesn't exist")

    def get(self, request, *args, **kwargs):
        team_id = int(self.kwargs["team_id"])
        team = get_object_or_404(Team, pk=team_id)
        self.check_scope(request, team)

        users = team.users.all()

        return JsonResponse({"users": [model_to_dict(user) for user in users]})

    def post(self, request, *args, **kwargs):
        team_id = int(self.kwargs["team_id"])
        team = get_object_or_404(Team, pk=team_id)
        self.check_scope(request, team)

        user_info = json.loads(request.body.decode("utf-8"))
        if not validate_presence(user_info, ["email"]):
            return JsonResponse({"error": "Invalid User JSON data"}, status=400)

        cleaned_user_info = clean(user_info, ["first_name", "last_name", "email"])
        try:
            user = User.objects.get(email=cleaned_user_info["email"])
        except ObjectDoesNotExist:
            user = User.objects.create(username=cleaned_user_info["email"], **cleaned_user_info)

        if user.email in [u.email for u in team.users.all()]:
            return JsonResponse({"error": "User already on team"}, status=400)

        team.users.add(user)

        return JsonResponse({"user": model_to_dict(user)})

    def delete(self, request, *args, **kwargs):
        pass


@method_decorator(login_required, name='dispatch')
class ReportView(View):
    def get(self, request, *args, **kwargs):
        team_id = int(self.kwargs["team_id"])
        team = get_object_or_404(Team, pk=team_id)
        self.check_scope(request, team)
        report = team.report_set.first()
        questions = report.questions.all()

        return JsonResponse({"questions": [model_to_dict(q) for q in questions]})

    def post(self, request, *args, **kwargs):
        team_id = int(self.kwargs["team_id"])
        team = get_object_or_404(Team, pk=team_id)
        self.check_scope(request, team)

        report_info = json.loads(request.body.decode("utf-8"))
        validate_presence(report_info, ["question"])
        question_string = report_info["question"]
        question = Question.objects.create(text=question_string, report=team.report_set.first())

        return JsonResponse({"question": model_to_dict(question)})

    def delete(self, request, *args, **kwargs):
        question_id = int(self.kwargs["question_id"])
        question = get_object_or_404(Question, pk=question_id)
        team = question.report.team
        self.check_scope(request, team)

        question.active = False
        question.save()

        return JsonResponse({"question": question})


@method_decorator(login_required, name='dispatch')
class SurveyView(View):
    def get(self, request, *args, **kwargs):
        pass

@method_decorator(login_required, name='dispatch')
class RoleView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"roles": [model_to_dict(r) for r in Role.objects.all()]})
