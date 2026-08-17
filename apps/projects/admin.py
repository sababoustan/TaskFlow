from django.contrib import admin
from .models import Project, Status, Workflow, WorkflowStatus


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'workspace', 'workflow', 'name', 'description',
                    'start_date', 'end_date', 'created_at', 'updated_at',
                    'is_archived')
    list_filter = ('created_at', 'updated_at', 'is_archived')
    search_fields = (
        'name',
        'description',
        'workspace__title',
    )
    autocomplete_fields = ('workspace', 'workflow')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'workspace')
    search_fields = ('name', 'workspace')


@admin.register(WorkflowStatus)
class WorkflowStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'workflow', 'status', 'order')
    list_filter = ('workflow', 'status')
    search_fields = ('workflow__name', 'status__name')