from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    password1 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password1']

    def validate(self, attrs):
        password = attrs.get("password")
        password1 = attrs.get("password1")

        if password != password1:
            raise serializers.ValidationError(
                {"password1": "Passwords do not match."}
            )

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(
                {"password": list(e.messages)}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password1', None)
        return User.objects.create_user(**validated_data)