from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView


from .filters import QuestionFilter
from .models import (Customer, Feedback, Profession, Question,
                     QuestionAnswer, Worker)
from .serializers import (CustomerSerializer, FeedbackSerializer,
                          ProfessionSerializer, QuestionAnswerSerializer,
                          QuestionSerializer, WorkerCreateSerializer,
                          WorkerSerializer, ScheduleSerializer)


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


class QuestionAnswerViewSet(viewsets.ModelViewSet, UpdateAPIView):
    serializer_class = QuestionAnswerSerializer

    def get_object(self):
        telegram_id = self.request.data.get('customer')
        question_title = self.request.data.get('question')
        question = get_object_or_404(Question, title=question_title)
        obj = get_object_or_404(
            QuestionAnswer, customer__telegram_id=telegram_id, question=question
        )
        return obj

    def get_queryset(self):
        telegram_id = self.kwargs.get('telegram_id')
        customer = get_object_or_404(Customer, telegram_id=telegram_id)
        return customer.answers.all()

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        telegram_id = self.kwargs.get('telegram_id')
        if self.basename == 'schedule_worker':
            user = get_object_or_404(Worker, telegram_id=telegram_id)
        else:
            user = get_object_or_404(Customer, telegram_id=telegram_id)
        return user.schedules.all()

