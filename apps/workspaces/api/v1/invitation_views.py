from rest_framework.permissions import IsAuthenticated
from apps.workspaces.choices import Role
from rest_framework.exceptions import PermissionDenied
from apps.workspaces.permissions import has_workspace_role
from rest_framework import viewsets
from .serializers import InvitationCreateSerializer, InvitationSerializer
from apps.workspaces.models import WorkspaceInvitation, Workspace
from django.shortcuts import get_object_or_404
from apps.workspaces.services import (invite_user_to_workspace,
                                      accept_invitation, reject_invitation,
                                      cancel_invitation)
from rest_framework.response import Response
from rest_framework import status


class InvitationViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return InvitationCreateSerializer
        elif self.action == "list":
            return InvitationSerializer

    def create(self, request, workspace_id=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitation = invite_user_to_workspace(
            invited_by=request.user,
            workspace_id=workspace_id,
            validated_data=serializer.validated_data
        )

        return Response({
            "messages": "The user was successfully invited.",
            "id": invitation.id,
        }, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return WorkspaceInvitation.objects.filter(
            workspace=self.kwargs["workspace_id"])

    def list(self, request, workspace_id=None):
        workspace = get_object_or_404(
            Workspace,
            id=workspace_id,
        )
        has_workspace_role(
            workspace=workspace,
            user=request.user,
            allowed_roles=[Role.ADMIN],
            )
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(
            {
                "data": serializer.data,
            }, status=status.HTTP_200_OK
        )

    def accept(self, request, pk=None):
        invitation = get_object_or_404(WorkspaceInvitation, pk=pk)
        if invitation.user != request.user:
            raise PermissionDenied(
                "You cannot accept another user's invitation."
            )
        membership = accept_invitation(
                invitation=invitation,
            )
        return Response(
            {
                "message": "Invitation accepted successfully.",
                "workspace": membership.workspace.id,
            },
            status=status.HTTP_201_CREATED,
        )

    def reject(self, request, pk=None):
        invitation = get_object_or_404(WorkspaceInvitation, pk=pk)
        if invitation.user != request.user:
            raise PermissionDenied(
                "You cannot reject another user's invitation."
            )
        invitation = reject_invitation(
                invitation=invitation,
            )
        return Response(
            {
                "message": "Invitation rejected successfully.",
                "workspace": invitation.workspace.id,
                "status": invitation.status,
            },
            status=status.HTTP_200_OK,
        )

    def cancel(self, request, pk=None):
        invitation = get_object_or_404(WorkspaceInvitation, pk=pk)
        has_workspace_role(
            workspace=invitation.workspace,
            user=request.user,
            allowed_roles=[Role.ADMIN],
            )
        invitation = cancel_invitation(
            invitation=invitation,
        )
        return Response(
            {
                "message": "Invitation cancelled successfully.",
                "workspace": invitation .workspace.id,
                "status": invitation.status,
            },
            status=status.HTTP_200_OK,
        )