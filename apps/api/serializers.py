from rest_framework import serializers


class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    result = serializers.CharField(required=True)


class ErrorResponseSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    error = serializers.CharField(required=True)
