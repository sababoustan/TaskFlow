from .models import Workflow, Status, WorkflowStatus
from apps.workspaces.models import Workspace
from .models import Project
from apps.workspaces.choices import Role
from apps.workspaces.permissions import has_workspace_role
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class WorkflowService:

    @staticmethod
    def create_workflow(*, user, workspace_id, data):
        name = data["name"]
        workspace = get_object_or_404(
            Workspace,
            id=workspace_id,
        )
        has_workspace_role(user=user, workspace=workspace,
                           allowed_roles=[Role.ADMIN, Role.MANAGER])
        if name in Workflow.objects.filter(name=name):
            return ValueError({"This workflow has already been created."})
        if name in Workflow.objects.filter(name=name):
            return ValidationError({
                "This workflow has already been created."
                })

        return Workflow.objects.create(
            workspace=workspace,
            name=name,
            )

    def update_workflow(*, user, workspace_id, workflow_id, name):
        workflow = get_object_or_404(
            Workflow,
            workspace=workspace_id,
            id=workflow_id
        )
        workspace = get_object_or_404(
            Workspace,
            id=workspace_id,
        )
        has_workspace_role(user=user, workspace=workspace,
                           allowed_roles=[Role.ADMIN, Role.MANAGER])        
        if Workflow.objects.filter(
            workspace=workspace,
            name=name,
        ).exclude(id=workflow_id).exists():
            raise ValidationError(
                {"detail": "This workflow already exists."}
            )
        workflow.name = name
        workflow.save(update_fields=["name"])
        return workflow

    def destroy(*, user, workspace_id, workflow_id):
        workflow = get_object_or_404(
            Workflow,
            workspace=workspace_id,
            id=workflow_id
        )
        workspace = get_object_or_404(
            Workspace,
            id=workspace_id,
        )
        has_workspace_role(user=user, workspace=workspace,
                           allowed_roles=[Role.ADMIN])
        if Project.objects.filter(workflow=workflow_id).exists():
            raise ValidationError({"detail": "This workflow is project-dependent and cannot be deleted."})

        workflow.delete()


class ProjectService:

    def create(*, user, workspace_id, workflow_id, data):
        name = data["name"]
        description = data["description"]
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        workspace = get_object_or_404(
            Workspace,
            id=workspace_id
        )
        workflow = get_object_or_404(
            Workflow,
            workspace=workspace_id,
            id=workflow_id
        )
        has_workspace_role(
            user=user,
            workspace=workspace,
            allowed_roles=[Role.ADMIN, Role.MANAGER]
        )
        return Project.objects.create(
            workspace=workspace,
            workflow=workflow,
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date
        )

    def update(*, user, workspace_id, project_id, data):
        workspace = get_object_or_404(
            Workspace,
            id=workspace_id
        )
        project = get_object_or_404(
            Project,
            workspace=workspace,
            id=project_id,
            )
        has_workspace_role(
            user=user,
            workspace=workspace,
            allowed_roles=[Role.ADMIN, Role.MANAGER]
        )

        for field, value in data.items():
            setattr(project, field, value)
        project.save(update_fields=data.keys())
        return project


class WorkflowStatusService:

    @staticmethod
    def create_workflow_status(*, user, workflow_id, data):
        status_id = data["status_id"]
        order = data["order"]
        workflow = get_object_or_404(
            Workflow,
            id=workflow_id
        )
        status = get_object_or_404(
            Status,
            id=status_id
        )
        has_workspace_role(user=user, workspace=workflow.workspace,
                           allowed_roles=[Role.ADMIN, Role.MANAGER])
        if WorkflowStatus.objects.filter(
            workflow=workflow,
            order=order
        ).exists():
            raise ValidationError({
                "detail": "This order is already used in this workflow."
            })
        return WorkflowStatus.objects.create(
            workflow=workflow,
            status=status,
            order=order,
            )

    def update_workflow_status(*, user,  workflow_status_id, order):
        workflow_status = get_object_or_404(
            WorkflowStatus,
            id=workflow_status_id,
        )
        has_workspace_role(user=user,
                           workspace=workflow_status.workflow.workspace,
                           allowed_roles=[Role.ADMIN, Role.MANAGER])
        if workflow_status.order == order:
            raise ValidationError({
                "detail": "This workflow status already has this order."
            })      
        if WorkflowStatus.objects.filter(
            workflow=workflow_status.workflow,
            order=order,
        ).exclude(id=workflow_status.id).exists():
            raise ValidationError(
                {"detail": "This workflow has already been registered for this order."}
            )
        workflow_status.order = order
        workflow_status.save(update_fields=["order"])
        return workflow_status

    def destroy_workflow_status(*, user, workflow_status_id):
        workflow_status = get_object_or_404(
            WorkflowStatus,
            id=workflow_status_id,
        )
        has_workspace_role(user=user,
                           workspace=workflow_status.workflow.workspace,
                           allowed_roles=[Role.ADMIN])

        workflow_status.delete()