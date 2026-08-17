from django.contrib import admin

from .models import Membership, Workspace, WorkspaceInvitation

# Register your models here.


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "created_at", "slug")
    list_filter = ("title", "owner__email")
    search_fields = (
        "title",
        "created_at",
    )
    readonly_fields = ("created_at", "slug")


@admin.register(Membership)
class MembershipeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "workspace", "role", "joined_at")
    list_filter = ("role", "joined_at")
    search_fields = (
        "user__email",
        "workspace__title",
    )
    readonly_fields = ("joined_at",)


@admin.register(WorkspaceInvitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invited_by",
        "workspace",
        "user",
        "role",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at", "role")
    search_fields = (
        "user__email",
        "workspace__title",
        "invited_by__email",
    )
    autocomplete_fields = ("invited_by", "user", "workspace")
    readonly_fields = ("created_at",)
