from rest_framework import serializers


class GitHubOAuthCallbackSerializer(serializers.Serializer):
    code = serializers.CharField()


class GitHubOAuthResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.DictField()
