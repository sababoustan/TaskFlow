from django.urls import path, include
from .workspace_views import WorkspaceViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api/v1'

router = DefaultRouter()
router.register('', WorkspaceViewSet, basename='workspace')

urlpatterns = [
    path('', include(router.urls)),
]