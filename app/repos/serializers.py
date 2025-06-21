from rest_framework import serializers
from .models import Repo


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = [
            'name',
            'url',
            'stars',
            'forks',
            'langs',
            'domains',
            'good_first'
        ]
