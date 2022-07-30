from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProfessionViewSet, WorkerViewSet, CustomerViewSet, FeedbackViewSet

router_v1 = DefaultRouter()

router_v1.register(
    'professions', ProfessionViewSet,
    basename='professions'
)
router_v1.register(
    'workers', WorkerViewSet,
    basename='workers'
)
router_v1.register(
    'customers', CustomerViewSet,
    basename='customers'
)
router_v1.register(
    'feedbacks', FeedbackViewSet,
    basename='feedbacks'
)

urlpatterns = [
    path('v1/', include(router_v1.urls), name='router_v1')
]
