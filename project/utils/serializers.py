from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    details = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField()),
        required=False,
        help_text="Field-level validation errors",
    )
