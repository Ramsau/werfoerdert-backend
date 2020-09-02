from django.db.models import Q, When, Case, Value as V, F, Count, Subquery
from django.db.models import CharField, DateField, IntegerField, BooleanField

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

import datetime

from .models import Question, Requirement, Grant
from .serializers import QuestionnaireSerializer


class QuestionnaireViewSet(viewsets.ViewSet):

    @action(methods=['get', 'post'], detail=False, url_path='next', url_name='')
    def get_questions(self, request):
        if request.method == 'POST':
            data = request.data

            answered_questions = Question.objects.filter(
                id__in=data.keys()
            )

            # annotate answers to the requirements
            whens_int = [
                When(
                    Q(question__id=k, question__type__id=1),
                    then=V(v if str(v).isdigit() else 0, output_field=IntegerField())
                ) for k, v in data.items()
            ]
            whens_bool = [
                When(
                    Q(question__id=k, question__type__id=2),
                    then=V(v is True, output_field=BooleanField())
                ) for k, v in data.items()
            ]
            requirements_answered = Requirement.objects.filter(
                question__id__in=answered_questions,
            ).annotate(
                answer_int=Case(
                    *whens_int,
                    default=None,
                    output_field=IntegerField(),
                ),
                answer_bool=Case(
                    *whens_bool,
                    default=None,
                    output_field=BooleanField(),
                ),
            )

            # filter requirements by whether boundaries were met
            requirements_met = requirements_answered.filter(
                Q(
                    Q(int_exact__isnull=True) |
                    Q(answer_int=F('int_exact'))
                ),
                Q(
                    Q(int_lt__isnull=True) |
                    Q(answer_int__lt=F('int_lt'))
                ),
                Q(
                    Q(int_gt__isnull=True) |
                    Q(answer_int__gt=F('int_gt'))
                ),
                Q(
                    Q(bool__isnull=True) |
                    Q(answer_bool=F('bool'))
                ),
            )

            requirements_unmet = requirements_answered.filter(~Q(id__in=requirements_met))
            requirements_open = Requirement.objects.filter(~Q(id__in=requirements_answered))

            # some requirements were met, the others unset
            grants_partiallyMet = Grant.objects.filter(
                ~Q(requirements__in=requirements_unmet),  # filter out grants where a requirement is known to be unmet
                Q(expires__gte=datetime.date.today()) | Q(expires__isnull=True),
            )
            # all requirements were met
            grants_fullyMet = grants_partiallyMet.filter(
                ~Q(requirements__in=requirements_open)
            )
        else:
            data = {}
            grants_partiallyMet = Grant.objects.filter(
                Q(expires__gte=datetime.date.today()) | Q(expires__isnull=True)
            )
            grants_fullyMet = grants_partiallyMet.filter(requirements__isnull=True)
            requirements_open = Requirement.objects.all()

        # get next grant/category to ask questions for: parent category has to be fully met to go on
        # or it has to be a starting category
        grants_next = grants_partiallyMet.filter(
            ~Q(id__in=grants_fullyMet),
            Q(
                Q(parent__in=grants_fullyMet) |
                Q(parent__isnull=True)
            )
        ).annotate(openrequirements_count=V(
            requirements_open.filter(grant__id=F('id')).count(),
            output_field=IntegerField()
        )).order_by('openrequirements_count')

        if grants_next.exists():
            grant = grants_next.first()
        else:
            grant = None


        serializer = QuestionnaireSerializer(current_grant=grant, grants_met=grants_fullyMet.filter(is_grant=True))
        return Response(serializer.data)
