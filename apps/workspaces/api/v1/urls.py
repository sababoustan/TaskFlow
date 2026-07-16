from django.urls import path, include
from .workspace_views import WorkspaceViewSet
from .invitation_views import InvitationApi
from rest_framework.routers import DefaultRouter

app_name = 'api/v1'

router = DefaultRouter()
router.register('', WorkspaceViewSet, basename='workspace')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:workspace_id>/invitations/', InvitationApi.as_view(),
         name="workspace-invitations")
]