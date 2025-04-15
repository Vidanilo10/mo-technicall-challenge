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
from .models import Loan, Payment, PaymentDetail


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
        loan_external_id = request.data.get("loan_external_id")
        loan = Loan.objects.get(external_id_character=loan_external_id)
        loan_amount = loan.amount

        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            total_debt = Loan.objects.filter(external_id_character=loan_external_id).aggregate(total_amount=Sum('outstanding'))

            if total_debt:
                if request.data.get("total_amount") <= total_debt.get("total_amount"):
                    serializer.save()

                    payment = Payment.objects.get(external_id_character=request.data.get("external_id_character"))

                    new_payment_detail = PaymentDetail(
                        amount = request.data.get("total_amount"),
                        loan = loan,
                        payment = payment
                    )

                    new_payment_detail.save()


                    total_amount_dict = PaymentDetail.objects.filter(loan_id=loan_external_id).aggregate(total_amount=Sum('amount'))
                    total_amount = total_amount_dict.get("total_amount")

                    outstanding = loan_amount - total_amount


                    if outstanding <= 0:
                        loan_status  = 4
                    else:
                        loan_status = 1
                    
                    loan.status = loan_status
                    loan.outstanding = outstanding
                    loan.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
