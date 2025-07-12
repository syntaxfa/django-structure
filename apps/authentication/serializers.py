from rest_framework import serializers

from apps.api.serializers import SuccessResponseSerializer


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class GenerateTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(default="refresh_token")
    access_token = serializers.CharField(default="access_token")
    expired_at = serializers.IntegerField(default=120)


class TokenVerifyResponseSerializer(SuccessResponseSerializer):
    message = serializers.CharField(default="Token successfully verified.")
    result = serializers.CharField(default="")


class TokenRefreshResponseSerializer(SuccessResponseSerializer):
    message = serializers.CharField(default="Token refreshed.")
    result = GenerateTokenSerializer()


class TokenBanResponseSerializer(SuccessResponseSerializer):
    message = serializers.CharField(default="user logged out.")
    result = serializers.CharField(default="")
