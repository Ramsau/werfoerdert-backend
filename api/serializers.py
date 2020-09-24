from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Grant, Question


class GrantSerializerQuestions(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = ['id', 'is_grant', 'name_de', 'name_en', 'parent', 'expires', 'questions']
        depth = 1


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = ['id', 'is_grant', 'name_de', 'name_en', 'parent', 'expires']
        depth = 1


class QuestionnaireSerializer(serializers.Serializer):
    current_grant = GrantSerializerQuestions()
    grants_met = GrantSerializer(many=True)


    def __init__(self, **kwargs):
        # cast keyword arguments to dict
        super().__init__(kwargs)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text_de', 'text_en', 'type']
        depth = 0


class AdminGrantSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_grant = serializers.BooleanField()
    name_de = serializers.CharField()
    name_en = serializers.CharField()
    expires = serializers.DateField()
    children = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'is_grant', 'name_de', 'name_en', 'expires', 'children']
        depth = 0

    def get_children(self, grant):
        serializer = AdminGrantSerializer(grant.children, many=True)
        return serializer.data

