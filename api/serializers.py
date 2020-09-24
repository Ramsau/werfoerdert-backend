from rest_framework import serializers

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


class AdminGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = ['id', 'is_grant', 'name_de', 'name_en', 'parent', 'expires','children']
        depth = 5
