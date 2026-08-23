import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.projects.models import Project, Status, Workflow, WorkflowStatus, Sprint
from apps.workspaces.models import Membership, Role, Workspace


@pytest.fixture
def admin_user(db):
    User = get_user_model()

    return User.objects.create_user(
        email="admin@gmail.com",
        full_name="Admin User",
        password="StrongPassword123",
        is_verified=True,
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def workspace_member(db, another_user, workspace):
    return Membership.objects.create(
        user=another_user,
        workspace=workspace,
        role=Role.MEMBER,
    )


@pytest.fixture
def workspace_admin(db, another_user, workspace):
    return Membership.objects.create(
        user=another_user,
        workspace=workspace,
        role=Role.ADMIN,
    )


@pytest.fixture
def workspace_manager(db, another_user, workspace):
    return Membership.objects.create(
        user=another_user,
        workspace=workspace,
        role=Role.MANAGER,
    )


@pytest.fixture
def workspace_viewer(db, another_user, workspace):
    return Membership.objects.create(
        user=another_user,
        workspace=workspace,
        role=Role.VIEWER,
    )


@pytest.fixture
def status_obj(db):
    return Status.objects.create(name="To Do")


@pytest.fixture
def status_obj_another(db):
    return Status.objects.create(name="Done")


@pytest.fixture
def workflow(db, workspace):
    return Workflow.objects.create(
        workspace=workspace,
        name="Development",
    )


@pytest.fixture
def workflow_another(db, another_workspace):
    return Workflow.objects.create(
        workspace=another_workspace,
        name="Software Development",
    )

@pytest.fixture
def workflow_same_workspace(db, workspace):
    return Workflow.objects.create(
        workspace=workspace,
        name="Software Development",
    )

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def project(db, workspace, workflow):
    return Project.objects.create(
        workspace=workspace,
        workflow=workflow,
        name="E-commerce Platform",
        description="Develop the backend and API for the e-commerce platform.",
    )


@pytest.fixture
def another_project(db, another_user, another_workspace, workflow_another):
    return Project.objects.create(
        workspace=another_workspace,
        workflow=workflow_another,
        name="Backend",
        description="Form login.",
    )


@pytest.fixture
def workflow_status(db, workflow, status_obj):
    return WorkflowStatus.objects.create(workflow=workflow, status=status_obj, order=1)


@pytest.fixture
def workflow_status_another(db, workflow_another, status_obj):
    return WorkflowStatus.objects.create(
        workflow=workflow_another, status=status_obj, order=1
    )


@pytest.fixture
def sprint(db, project):
    return Sprint.objects.create(
        project=project,
        name="Sprint 1",
        start_date="2026-08-19",
        end_date="2026-09-19",
        goal="Complete authentication and project management features."
    )

@pytest.fixture
def sprint_another(db, project):
    return Sprint.objects.create(
        project=project,
        name="Sprint 2",
    )


@pytest.fixture
def membership_factory(db, another_user, workspace):

    def create_membership(role):
        return Membership.objects.create(
            user=another_user,
            workspace=workspace,
            role=role,
        )

    return create_membership
