from django.contrib import admin

from .models import Group, Question, Survey, Answer


class GroupAdmin(admin.ModelAdmin):
    raw_id_fields = ('admin', )

class QuestionAdmin(admin.ModelAdmin):
    pass

class SurveyAdmin(admin.ModelAdmin):
    pass

class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Answer, AnswerAdmin)