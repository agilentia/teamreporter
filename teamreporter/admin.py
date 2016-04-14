from django.contrib import admin

from .models import Team, Question, Survey, Answer, Report, DailyReport


class SurveyInline(admin.StackedInline):
    model = Survey


class QuestionAdmin(admin.ModelAdmin):
    pass


class MembershipInline(admin.TabularInline):
    model = Team.users.through
    raw_id_fields = ('user',)


class TeamAdmin(admin.ModelAdmin):
    raw_id_fields = ('admin',)
    inlines = (MembershipInline,)


class SurveyAdmin(admin.ModelAdmin):
    pass


class AnswerAdmin(admin.ModelAdmin):
    pass


class DailyReportInline(admin.TabularInline):
    model = DailyReport
    extra = 1


class ReportAdmin(admin.ModelAdmin):
    inlines = (DailyReportInline,)


admin.site.register(Report, ReportAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Answer, AnswerAdmin)
