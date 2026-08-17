from django.db import models
from django.utils.text import slugify

from apps.users.models import User
from apps.workspaces.choices import InvitationStatus, Role

# Create your models here.


class Workspace(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_workspaces"
    )
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title, allow_unicode=True)
            unique_slug = slug
            counter = 1
            ModelClass = self.__class__
            while ModelClass._default_manager.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}-{counter}"
                counter += 1

            self.slug = unique_slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner}-{self.title}"


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "workspace"],
                name="unique_workspace_member",
            )
        ]
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user}-{self.workspace}"


class WorkspaceInvitation(models.Model):
    invited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_invitations"
    )
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="invitations"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitations")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    status = models.CharField(
        max_length=10,
        choices=InvitationStatus.choices,
        default=InvitationStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "workspace"],
                name="unique_workspace_invitation",
                condition=models.Q(status=InvitationStatus.PENDING),
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user}-{self.workspace}"
