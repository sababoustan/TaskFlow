from django.urls import path, include
from .workspace_views import WorkspaceViewSet
from .invitation_views import InvitationViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api/v1'

router = DefaultRouter()
router.register('', WorkspaceViewSet, basename='workspace')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:workspace_id>/invitations/',
         InvitationViewSet.as_view({"get": "list", "post": "create"}),
         ),
    path('invitations/<int:pk>/accept/',
         InvitationViewSet.as_view({
             "post": "accept",
         }),
         ),
    path('invitations/<int:pk>/reject/',
         InvitationViewSet.as_view({
            "post": "reject",
         }),
         ),
    path('invitations/<int:pk>/cancel/',
         InvitationViewSet.as_view({
            "post": "cancel",
         }),
         ),
]