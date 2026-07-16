from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import InvitationsSerializer
from apps.workspaces.services import invite_user_to_workspace
from rest_framework.response import Response
from rest_framework import status


class InvitationApi(APIView):
    serializer_class = InvitationsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("Invitation API")
        print(request.user)
        workspace_id = kwargs["workspace_id"]
        serializer = self.serializer_class(data=request.data)
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