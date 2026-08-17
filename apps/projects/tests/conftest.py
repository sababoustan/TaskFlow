import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.projects.models import Status, Workflow, Project, WorkflowStatus
from apps.workspaces.models import Workspace, Membership, Role


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def another_user(db):
    User = get_user_model()

    return User.objects.create_user(
        email="another@gmail.com",
        full_name="Another User",
        password="StrongPassword123",
        is_verified=True,
    )


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
def another_workspace(db, another_user):
    return Workspace.objects.create(
        owner=another_user,
        title="Another Workspace",
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
def status_obj(db):
    return Status.objects.create(
        name="To Do"
    )


@pytest.fixture
def status_obj_another(db):
    return Status.objects.create(
        name="Done"
    )


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
        name="	Software Development",
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
def workflow_status(db, workflow, status_obj):
    return WorkflowStatus.objects.create(
        workflow=workflow,
        status=status_obj,
        order=1
    )


@pytest.fixture
def workflow_status_another(db, workflow_another, status_obj):
    return WorkflowStatus.objects.create(
        workflow=workflow_another,
        status=status_obj,
        order=1
    )
