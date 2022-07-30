from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .models import (Choice, Customer, Feedback, Profession, Question,
                     QuestionAnswer, Worker, Schedule)
from .serializers import ProfessionSerializer, WorkerSerializer, WorkerCreateSerializer


class ProfessionViewSet(ReadOnlyModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class WorkerViewSet(ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', ):
            return WorkerCreateSerializer
        return WorkerSerializer
