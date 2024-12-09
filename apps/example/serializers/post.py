from rest_framework import serializers

from apps.example.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "title", "description")
