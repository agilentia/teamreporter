from django.contrib import admin

from .models import Team as Group, Question, Survey, Answer


class SurveyInline(admin.StackedInline):
    model = Survey


class GroupAdmin(admin.ModelAdmin):
    raw_id_fields = ('admin',)


class QuestionAdmin(admin.ModelAdmin):
    pass


class SurveyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('group', 'user', 'date')}


class AnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Answer, AnswerAdmin)
