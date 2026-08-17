from django.db import models

from apps.workspaces.models import Workspace


# Create your models here.
class Project(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="projects"
    )
    workflow = models.ForeignKey(
        "Workflow", on_delete=models.PROTECT, related_name="projects"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "name"],
                name="unique_workspace_project_name",
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}"


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    def __str__(self):
        return f"{self.name}"


class Workflow(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class WorkflowStatus(models.Model):
    workflow = models.ForeignKey(
        Workflow, on_delete=models.CASCADE, related_name="workflow_statuses"
    )
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, related_name="workflow_statuses"
    )
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["workflow", "status"], name="unique_workflow_status"
            ),
            models.UniqueConstraint(
                fields=["workflow", "order"],
                name="unique_workflow_order",
            ),
        ]

    def __str__(self):
        return f"{self.workflow.name} - {self.status.name}"
