import django_filters as df

from .models import Question, QuestionAnswer, Worker, Feedback, Profession


class QuestionAnswerFilter(df.FilterSet):
    profession = df.CharFilter(field_name='question__profession__title', lookup_expr='contains')

    class Meta:
        model = QuestionAnswer
        fields = ('profession', )


class QuestionFilter(df.FilterSet):
    profession = df.CharFilter(field_name='profession__title', lookup_expr='contains')

    class Meta:
        model = Question
        fields = ('profession', )


class WorkersFilter(df.FilterSet):

    class Meta:
        model = Worker
        fields = ('telegram_id', )


class FeedbackFilter(df.FilterSet):
    worker = df.CharFilter(field_name='worker__telegram_id', lookup_expr='contains')

    class Meta:
        model = Feedback
        fields = ('worker', )

