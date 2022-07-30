from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import (Choice, Customer, Feedback, Profession, Question,
                     QuestionAnswer, Schedule, Worker)
from .serializers import (CustomerSerializer, ProfessionSerializer,
                          WorkerCreateSerializer, WorkerSerializer,
                          FeedbackSerializer)


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


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
