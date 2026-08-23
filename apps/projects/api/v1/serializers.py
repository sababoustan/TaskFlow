from rest_framework import serializers

from ...models import Project, Status, Workflow, WorkflowStatus, Sprint


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name"]


class WorkflowListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = ["id", "name", "workspace"]
        read_only_fields = ["workspace"]


class WorkflowCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Workflow
        fields = ["name"]


class WorkflowUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = [
            "name",
        ]


class ProjectListSerializer(serializers.ModelSerializer):
    workspace_id = serializers.CharField(source="workspace.id", read_only=True)
    workflow_id = serializers.CharField(source="workflow.id", read_only=True)

    class Meta:
        model = Project
        fields = ["id", "workspace_id", "workflow_id", "name", "is_archived"]


class ProjectCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    start_date = serializers.DateTimeField(required=False, allow_null=True)
    end_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
        ]


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "is_archived"
            ]


class WorkflowStatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStatus
        fields = ["workflow", "status", "order"]


class WorkflowStatusCreateSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField()
    status_id = serializers.IntegerField()

    class Meta:
        model = WorkflowStatus
        fields = ["status_id", "order"]


class WorkflowStatusUpdateSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField()

    class Meta:
        model = WorkflowStatus
        fields = ["order"]


class SprintListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ["name", "start_date", "end_date", "goal"]


class SprintCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    start_date = serializers.DateTimeField(
        required=False,
        allow_null=True
    )
    end_date = serializers.DateTimeField(
        required=False,
        allow_null=True
    )
    goal = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )
    
    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "end_date": "End date must be after start date."
            })

        return attrs

    class Meta:
        model = Sprint
        fields = ["name", "start_date", "end_date", "goal"]


class SprintUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    start_date = serializers.DateTimeField(
        required=False,
        allow_null=True
    )
    end_date = serializers.DateTimeField(
        required=False,
        allow_null=True
    )
    goal = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )

    def validate(self, attrs):
        start_date = attrs.get("start_date", self.instance.start_date)
        end_date = attrs.get("end_date", self.instance.end_date)

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "end_date": "End date must be after start date."
            })

        return attrs

    class Meta:
        model = Sprint
        fields = ["name", "start_date", "end_date", "goal"]
