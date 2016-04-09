from django.contrib import admin

from .models import Team as Group, Question, Survey, Answer, Membership, Report


class SurveyInline(admin.StackedInline):
    model = Survey


class GroupAdmin(admin.ModelAdmin):
    raw_id_fields = ('admin',)


class QuestionAdmin(admin.ModelAdmin):
    pass


class MembershipAdmin(admin.ModelAdmin):
    pass


class SurveyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('report', 'user', 'date')}


class AnswerAdmin(admin.ModelAdmin):
    pass


class ReportAdmin(admin.ModelAdmin):
    pass


admin.site.register(Report, ReportAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Answer, AnswerAdmin)
