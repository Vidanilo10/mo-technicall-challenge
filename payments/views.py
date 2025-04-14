from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from drf_yasg import openapi

from django.db.models import Sum

from .serializers import PaymentSerializer
from .models import Loan, Payment


class PaymentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A simple ViewSet for create and query payment by customer.
    """
    queryset = Payment.objects.all()
    serializer = PaymentSerializer(queryset, many=True)
    serializer_class = PaymentSerializer

    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer']

    def create(self, request):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            total_debt = Loan.objects.filter(customer_id=request.data.get("customer")).aggregate(
                total_amount=Sum('outstanding'))

            if total_debt:
                if request.data.get("total_amount") <= total_debt.get("total_amount"):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
