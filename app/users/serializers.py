from rest_framework import serializers
from users.models import User


class UserPreferencesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pref_langs', 'pref_domains']
