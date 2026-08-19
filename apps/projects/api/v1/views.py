from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.workspaces.choices import Role
from apps.workspaces.models import Workspace
from apps.workspaces.permissions import has_workspace_role

from ...models import Project, Status, Workflow, WorkflowStatus, Sprint
from ...services import (
    ProjectService,
    WorkflowService,
    WorkflowStatusService,
    SprintService
)
from .serializers import (
    ProjectCreateSerializer,
    ProjectListSerializer,
    ProjectUpdateSerializer,
    StatusSerializer,
    WorkflowCreateSerializer,
    WorkflowListSerializer,
    WorkflowStatusCreateSerializer,
    WorkflowStatusListSerializer,
    WorkflowStatusUpdateSerializer,
    WorkflowUpdateSerializer,
    SprintListSerializer,
    SprintCreateSerializer,
    SprintUpdateSerializer
)


class StatusViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class WorkflowViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return WorkflowListSerializer
        elif self.action == "create":
            return WorkflowCreateSerializer
        elif self.action == "update":
            return WorkflowUpdateSerializer

    def get_queryset(self):
        return Workflow.objects.filter(
            workspace=self.kwargs.get("workspace_id")
        ).distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workflow = WorkflowService.create(
            user=self.request.user,
            workspace_id=self.kwargs.get("workspace_id"),
            data=serializer.validated_data,
        )
        return Response(
            {
                "messages": "Workflow created successfully.",
                "id": workflow.id,
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        workspace = get_object_or_404(Workspace, id=self.kwargs.get("workspace_id"))
        has_workspace_role(
            user=request.user,
            workspace=workspace,
            allowed_roles=[
                Role.ADMIN,
                Role.MANAGER,
                Role.MEMBER,
                Role.VIEWER,
            ],
        )
        workflows = self.get_queryset()

        serializer = self.get_serializer(workflows, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, workflow_id=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workflow = WorkflowService.update(
            user=self.request.user,
            workspace_id=self.kwargs.get("workspace_id"),
            workflow_id=workflow_id,
            name=serializer.validated_data["name"],
        )
        return Response(
            {
                "message": "Workflow updated successfully.",
                "data": WorkflowListSerializer(workflow).data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, workflow_id=None, *args, **kwargs):
        WorkflowService.destroy(
            user=request.user,
            workspace_id=self.kwargs.get("workspace_id"),
            workflow_id=workflow_id,
        )

        return Response(
            {
                "message": f"{request.user}successfully removed from the workflow.",
                "workflow": workflow_id,
            },
            status=status.HTTP_200_OK,
        )


class ProjectViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        elif self.action == "create":
            return ProjectCreateSerializer
        elif self.action == "update":
            return ProjectUpdateSerializer

    def get_queryset(self):
        return Project.objects.filter(
            workspace=self.kwargs.get("workspace_id")
        ).distinct()

    def list(self, request, *args, **kwargs):
        workspace = get_object_or_404(Workspace, id=self.kwargs.get("workspace_id"))
        has_workspace_role(
            user=request.user,
            workspace=workspace,
            allowed_roles=[
                Role.ADMIN,
                Role.MANAGER,
                Role.MEMBER,
                Role.VIEWER,
            ],
        )
        project = self.get_queryset()

        serializer = self.get_serializer(project, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = ProjectService.create(
            user=request.user,
            workspace_id=self.kwargs.get("workspace_id"),
            workflow_id=self.kwargs.get("workflow_id"),
            data=serializer.validated_data,
        )
        return Response(
            {"message": "The project was created successfully.",
             "id": project.id},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        project_update = ProjectService.update(
            user=request.user,
            workspace_id=self.kwargs.get("workspace_id"),
            project_id=self.kwargs.get("project_id"),
            data=serializer.validated_data,
        )
        return Response(
            {
                "message": "The project was updated successfully.",
                "id": project_update.id,
            },
            status=status.HTTP_200_OK,
        )


class WorkflowStatusViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return WorkflowStatusListSerializer
        elif self.action == "create":
            return WorkflowStatusCreateSerializer
        elif self.action == "update":
            return WorkflowStatusUpdateSerializer

    def get_queryset(self):
        return WorkflowStatus.objects.filter(
            workflow=self.kwargs.get("workflow_id"),
        ).distinct()

    def list(self, request, *args, **kwargs):
        workflow = get_object_or_404(Workflow, id=self.kwargs.get("workflow_id"))
        has_workspace_role(
            user=request.user,
            workspace=workflow.workspace,
            allowed_roles=[
                Role.ADMIN,
                Role.MANAGER,
                Role.MEMBER,
                Role.VIEWER,
            ],
        )
        workflowstatus = self.get_queryset()

        serializer = self.get_serializer(workflowstatus, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workflow_status = WorkflowStatusService.create(
            user=request.user,
            workflow_id=self.kwargs.get("workflow_id"),
            data=serializer.validated_data,
        )
        return Response(
            {
                "message": "The workflow status was created successfully.",
                "id": workflow_status.id,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        workflow_status = WorkflowStatusService.update(
            user=request.user,
            workflow_status_id=self.kwargs.get("workflow_status_id"),
            order=serializer.validated_data["order"],
        )
        return Response(
            {
                "message": "The workflow status was updated successfully.",
                "id": workflow_status.id,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        workflow_status = WorkflowStatusService.destroy(
            user=request.user,
            workflow_status_id=self.kwargs.get("workflow_status_id"),
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class SprintViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return SprintListSerializer
        elif self.action == "create":
            return SprintCreateSerializer
        elif self.action == "retrieve":
            return SprintListSerializer
        elif self.action == "update":
            return SprintUpdateSerializer

    def get_queryset(self):
        return Sprint.objects.filter(
            project=self.kwargs.get("project_id"),
        ).distinct()

    def list(self, request, *args, **kwargs):
        project = get_object_or_404(
            Project,
            id=kwargs["project_id"],
            workspace_id=kwargs["workspace_id"],
        )
        has_workspace_role(
            user=request.user,
            workspace=project.workspace,
            allowed_roles=[
                Role.ADMIN,
                Role.MANAGER,
                Role.MEMBER,
                Role.VIEWER,
            ],
        )
        sprint = self.get_queryset()

        serializer = self.get_serializer(sprint, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sprint = SprintService.create(
            user=request.user,
            workspace_id=self.kwargs.get("workspace_id"),
            project_id=self.kwargs.get("project_id"),
            data=serializer.validated_data,
        )
        return Response(
            {
                "message": "The sprint was created successfully.",
                "id": sprint.id,
            },
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, *args, **kwargs):
        sprint = get_object_or_404(
            Sprint,
            id=kwargs["sprint_id"],
            project=kwargs["project_id"],
            project__workspace_id=kwargs["workspace_id"],
        )
        has_workspace_role(
            user=request.user,
            workspace=sprint.project.workspace,
            allowed_roles=[
                Role.ADMIN,
                Role.MANAGER,
                Role.MEMBER,
                Role.VIEWER,
            ],
        )
        serializer = self.get_serializer(sprint)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        sprint = SprintService.update(
            user=request.user,
            workspace_id=self.kwargs.get("workspace_id"),
            project_id=self.kwargs.get("project_id"),
            sprint_id=self.kwargs.get("sprint_id"),
            data=serializer.validated_data,
        )
        return Response(
            {
                "message": "The sprint was updated successfully.",
                "id": sprint.id,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        sprint = SprintService.destroy(
            user=request.user,
            workspace_id=self.kwargs.get("workspace_id"),
            project_id=self.kwargs.get("project_id"),
            sprint_id=self.kwargs.get("sprint_id"),
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
