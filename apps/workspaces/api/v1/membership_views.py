from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import MembershipListSerializer, MembershipUpdateSerializer
from apps.workspaces.models import Membership, Workspace
from apps.workspaces.permissions import has_workspace_role
from django.shortcuts import get_object_or_404
from apps.workspaces.choices import Role
from rest_framework.response import Response
from rest_framework import status
from apps.workspaces.services import update_membership_role, remove_workspace_member


class MembershipViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Membership.objects.filter(
            workspace=self.kwargs["workspace_id"])

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return MembershipListSerializer

        if self.action == "update":
            return MembershipUpdateSerializer

    def retrieve(self, request, workspace_id=None, member_id= None):
        workspace = get_object_or_404(
            Workspace,
            id=workspace_id
        )
        has_workspace_role(
            workspace=workspace,
            user=request.user,
            allowed_roles=[Role.ADMIN],
            )
        membership = get_object_or_404(
            Membership,
            workspace=workspace,
            id=member_id
        )
        serializer = self.get_serializer(membership)
        return Response(
            {
                "data": serializer.data,
            }, status=status.HTTP_200_OK
        )
        
    def list(self, request, workspace_id=None):
        workspace = get_object_or_404(
            Workspace,
            id=workspace_id
        )
        has_workspace_role(
            workspace=workspace,
            user=request.user,
            allowed_roles=[Role.ADMIN],
            )
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True,
        )
        return Response(
            {
                "data": serializer.data,
            }, status=status.HTTP_200_OK
        )

    def update(self, request, workspace_id=None, member_id=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        membership = get_object_or_404(
            Membership,
            workspace=workspace_id,
            id=member_id
        )
        membership = update_membership_role(
            membership=membership,
            updated_by=request.user,
            workspace_id=workspace_id,
            role=serializer.validated_data["role"],
        )
        return Response(
            {
                "message": "Member updated successfully.",
                "data": MembershipListSerializer(membership).data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, workspace_id=None, member_id=None):
        membership = get_object_or_404(
            Membership,
            workspace=workspace_id,
            id=member_id
        )
        remove_workspace_member(
            membership=membership,
            workspace_id=workspace_id,
            updated_by=request.user,
        )
        return Response(
            {
                "message": f"{membership.user.email} successfully removed from the workspace.",
                "workspace": membership.workspace.id,
            },
            status=status.HTTP_200_OK,
        )