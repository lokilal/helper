import django_filters as df

from .models import Question


class QuestionFilter(df.FilterSet):
    profession = df.CharFilter(field_name='profession__title', lookup_expr='contains')

    class Meta:
        model = Question
        fields = '__all__'
