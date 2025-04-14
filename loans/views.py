from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema # type: ignore
from drf_yasg import openapi

from django.db.models import Sum

from .serializers import LoanSerializer
from .models import Loan


class LoansViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A simple ViewSet for create and query loan by customer.
    """

    queryset = Loan.objects.all()
    serializer = LoanSerializer(queryset, many=True)
    serializer_class = LoanSerializer

    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer']
