from django.urls import path

from .views import (CustomerViewSet, FeedbackViewSet, ProfessionViewSet,
                    QuestionAnswerViewSet, QuestionViewSet, WorkerViewSet, ScheduleViewSet)

GENERAL_METHODS = {
            'get': 'list',
            'post': 'create',
            'patch': 'partial_update'
        }

urlpatterns = [
    path('v1/answers/', QuestionAnswerViewSet.as_view(
        GENERAL_METHODS
    ), name='answers'),
    path('v1/customers/', CustomerViewSet.as_view(
        GENERAL_METHODS
    ), name='customers'),
    path('v1/workers/', WorkerViewSet.as_view(
        GENERAL_METHODS
    ), name='workers'),
    path('v1/professions/', ProfessionViewSet.as_view(
        {'get': 'list'}
    ), name='professions'),
    path('v1/questions/', QuestionViewSet.as_view(
        {'get': 'list'}
    ), name='questions'),
    path('v1/feedbacks/', FeedbackViewSet.as_view(
        {'get': 'list'}
    ), name='feedbacks'),
    path('v1/schedule/', ScheduleViewSet.as_view(
        GENERAL_METHODS
    ), name='schedules')
]
