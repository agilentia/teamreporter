from django import forms


class SurveyForm(forms.Form):
    question_prefix = 'question'

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(SurveyForm, self).__init__(*args, **kwargs)

        for question in questions:
            self.fields['{0}{1}'.format(self.question_prefix, question.pk)] = \
                forms.CharField(label=question.text, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def extract_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith(self.question_prefix):
                yield (name.replace(self.question_prefix, ''), value)
