import django_filters as df

from .models import Question, QuestionAnswer


class QuestionAnswerFilter(df.FilterSet):
    profession = df.CharFilter(field_name='question__profession__title', lookup_expr='contains')

    class Meta:
        model = QuestionAnswer
        fields = '__all__'


class QuestionFilter(df.FilterSet):
    profession = df.CharFilter(field_name='profession__title', lookup_expr='contains')

    class Meta:
        model = Question
        fields = '__all__'
