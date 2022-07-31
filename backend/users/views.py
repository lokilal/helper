from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from django.shortcuts import get_object_or_404

from .filters import QuestionFilter
from .models import (Choice, Customer, Feedback, Profession, Question,
                     QuestionAnswer, Schedule, Worker)
from .serializers import (CustomerSerializer, FeedbackSerializer,
                          ProfessionSerializer, QuestionAnswerSerializer,
                          QuestionSerializer, WorkerCreateSerializer,
                          WorkerSerializer)


class ProfessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', ):
            return WorkerCreateSerializer
        return WorkerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = QuestionFilter


class QuestionAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionAnswerSerializer

    def get_queryset(self):
        telegram_id = self.kwargs.get('telegram_id')
        customer = get_object_or_404(Customer, telegram_id=telegram_id)
        return customer.answers.all()
