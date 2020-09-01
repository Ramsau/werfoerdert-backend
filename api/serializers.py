from rest_framework import serializers

from .models import Grant


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = ['id', 'is_grant', 'name_de', 'name_en', 'parent', 'expires', 'questions']
        depth = 1
