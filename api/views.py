from django.db.models import Q

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Question
from .serializers import QuestionSerializer

class QuestionViewSet(viewsets.ViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(methods=['get', 'post'], detail=False, url_path='next', url_name='')
    def get_questions(self, request):
        if request.method == 'POST':
            data = request.data
        else:
            data = {}

        queryset = self.queryset.filter(~Q(id__in=data.keys()))[:2]
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
