from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomerViewSet, FeedbackViewSet, ProfessionViewSet,
                    QuestionAnswerViewSet, QuestionViewSet, WorkerViewSet, ScheduleViewSet)

router_v1 = DefaultRouter()

router_v1.register(
    'professions', ProfessionViewSet,
    basename='professions'
)
router_v1.register(
    'workers/(?P<telegram_id>[^/.]+)', WorkerViewSet,
    basename='worker'
)
router_v1.register(
    'customers/(?P<telegram_id>[^/.]+)', CustomerViewSet,
    basename='customer'
)
router_v1.register(
    'feedbacks', FeedbackViewSet,
    basename='feedbacks'
)
router_v1.register(
    'questions', QuestionViewSet,
    basename='questions'
)
router_v1.register(
    'answers/(?P<telegram_id>[^/.]+)', QuestionAnswerViewSet,
    basename='answers'
)
router_v1.register(
    'schedule/worker/(?P<telegram_id>[^/.]+)', ScheduleViewSet,
    basename='schedule_worker'
)
router_v1.register(
    'schedule/customer/(?P<telegram_id>[^/.]+)', ScheduleViewSet,
    basename='schedule_customer'
)

urlpatterns = [
    path('v1/', include(router_v1.urls), name='router_v1')
]
