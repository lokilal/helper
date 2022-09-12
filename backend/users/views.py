from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from .filters import (QuestionFilter, QuestionAnswerFilter,
                      WorkersFilter, FeedbackFilter, ScheduleFilter,
                      CustomerFilter)
from .models import (Customer, Feedback, Profession, Question, Schedule,
                     QuestionAnswer, Worker)
from .serializers import (CustomerSerializer, FeedbackSerializer,
                          ProfessionSerializer, QuestionAnswerSerializer,
                          QuestionSerializer, WorkerCreateSerializer,
                          WorkerSerializer, ScheduleSerializer)


class ProfessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class WorkerViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = WorkersFilter

    def get_object(self):
        worker = get_object_or_404(
            Worker, telegram_id=self.request.data.get('telegram_id'))
        return worker

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return WorkerCreateSerializer
        return WorkerSerializer


class CustomerViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CustomerFilter
    pagination_class = LimitOffsetPagination
    paginate_by = 3

    def get_object(self):
        customer = get_object_or_404(
            Customer, telegram_id=self.request.data.get('telegram_id'))
        return customer


class FeedbackViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = FeedbackFilter


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = QuestionFilter


class QuestionAnswerViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = QuestionAnswerSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = QuestionAnswerFilter

    def get_object(self):
        telegram_id = self.request.data.get('customer')
        question_title = self.request.data.get('question')
        question = get_object_or_404(Question, title=question_title)
        obj = get_object_or_404(
            QuestionAnswer, customer__telegram_id=telegram_id, question=question
        )
        return obj

    def get_queryset(self):
        telegram_id = self.request.data.get('customer')
        customer = get_object_or_404(Customer, telegram_id=telegram_id)
        return customer.answers.all()

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ScheduleViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ScheduleFilter

    def get_object(self):
        worker = get_object_or_404(
            Worker, telegram_id=self.request.data.get('worker'))
        customer = get_object_or_404(
            Customer, telegram_id=self.request.data.get('customer'))
        obj = get_object_or_404(Schedule,
                                worker=worker, customer=customer)
        return obj
