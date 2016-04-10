from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Team, User, Question, Role, Membership, Report, Survey
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
        memberships = team.membership_set.all()
        users = []
        for m in memberships:  # TODO: make this little loop a method call on the object manager
            user_info = model_to_dict(m.user, fields=["email", "first_name", "last_name"])
            user_info["roles"] = [model_to_dict(r) for r in m.roles.all()]
            users.append(user_info)

        return JsonResponse({"users": users})

    def post(self, request, *args, **kwargs):
        team_id = int(self.kwargs["team_id"])
        team = get_object_or_404(Team, pk=team_id)
        self.check_scope(request, team)

        user_info = json.loads(request.body.decode("utf-8"))
        if not validate_presence(user_info, ["email", "roles"]):
            return JsonResponse({"error": "Invalid User JSON data"}, status=400)

        cleaned_user_info = clean(user_info, ["first_name", "last_name", "email", ])
        roles = [role["id"] for role in user_info["roles"]]
        try:
            user = User.objects.get(email=cleaned_user_info["email"])
        except ObjectDoesNotExist:
            user = User.objects.create(username=cleaned_user_info["email"], **cleaned_user_info)

        if team.users.filter(email=user.email).count():  # check if user in list already
            return JsonResponse({"error": "User already on team"}, status=400)

        membership = Membership.objects.create(team=team, user=user)
        membership.roles.add(*roles)
        membership.save()

        return JsonResponse({"user": model_to_dict(user, fields=['email', 'first_name', 'last_name'])})

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
        return JsonResponse({"roles": [model_to_dict(r, fields=["id", "name"]) for r in Role.objects.all()]})


@method_decorator(staff_member_required, name='dispatch')
class SummaryDebugPreview(TemplateView):
    template_name = 'email/summary.html'

    def get_context_data(self, **kwargs):
        context = super(SummaryDebugPreview, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['user_sent_report'] = Survey.objects.get(report=kwargs['report'],
                                                         user=self.request.user).completed is not None
        context['surveys'] = Report.objects.get(pk=kwargs['report']).survey_set.all()
        return context
