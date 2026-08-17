from rest_framework.exceptions import PermissionDenied

from apps.workspaces.models import Membership


def has_workspace_role(*, workspace, user, allowed_roles):
    """
    Check whether the user has one of the allowed roles
    in the given workspace.
    """

    if workspace.owner == user:
        return True

    has_role = Membership.objects.filter(
        workspace=workspace,
        user=user,
        role__in=allowed_roles,
    ).exists()

    if not has_role:
        raise PermissionDenied("You do not have permission to perform this action.")

    return True
