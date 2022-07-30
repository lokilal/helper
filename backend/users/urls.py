from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProfessionViewSet, WorkerViewSet

router_v1 = DefaultRouter()

router_v1.register(
    'professions', ProfessionViewSet,
    basename='professions'
)
router_v1.register(
    'workers', WorkerViewSet,
    basename='workers'
)

urlpatterns = [
    path('v1/', include(router_v1.urls), name='router_v1')
]
