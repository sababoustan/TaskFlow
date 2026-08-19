import pytest
from django.db import IntegrityError

from apps.projects.models import Project, Status, Workflow, WorkflowStatus, Sprint


@pytest.mark.django_db
class TestStatusModel:
    def test_create_status(self):
        status = Status.objects.create(name="In Progress")

        assert status.id is not None
        assert status.name == "In Progress"
        assert str(status) == "In Progress"

    def test_status_name_must_be_unique(self):
        Status.objects.create(name="Done")

        with pytest.raises(IntegrityError):
            Status.objects.create(name="Done")


@pytest.mark.django_db
def test_create_workflow(workspace):
    workflow = Workflow.objects.create(workspace=workspace, name="Development")

    assert workflow.id is not None
    assert workflow.name == "Development"
    assert workflow.workspace == workspace
    assert str(workflow) == "Development"


@pytest.mark.django_db
def test_create_project(workspace, workflow):
    project = Project.objects.create(
        workspace=workspace,
        workflow=workflow,
        name="E-commerce Platform",
        description="Develop the backend and API for the e-commerce platform.",
    )

    assert project.id is not None
    assert project.name == "E-commerce Platform"
    assert (
        project.description
        == "Develop the backend and API for the e-commerce platform."
    )
    assert project.workspace == workspace
    assert project.workflow == workflow
    assert str(project) == "E-commerce Platform"
    assert project.created_at is not None
    assert project.updated_at is not None
    assert project.is_archived is False


@pytest.mark.django_db
def test_create_workflow_status(workflow, status_obj):
    workflow_status = WorkflowStatus.objects.create(
        workflow=workflow, status=status_obj, order=1
    )

    assert workflow_status.id is not None
    assert workflow_status.workflow == workflow
    assert workflow_status.status == status_obj
    assert workflow_status.order == 1


@pytest.mark.django_db
def test_create_sprint(project):
    sprint = Sprint.objects.create(
        project=project,
        name="sprint 1",
        start_date="2026-08-19T08:03:25.955Z",
        end_date="2026-09-19T08:03:25.955Z",
        goal="Complete authentication and project management features."
    )

    assert sprint.id is not None
    assert sprint.project == project
    assert sprint.name == "sprint 1"
    assert sprint.start_date == "2026-08-19T08:03:25.955Z"
    assert sprint.end_date == "2026-09-19T08:03:25.955Z"
    assert sprint.goal == "Complete authentication and project management features."
