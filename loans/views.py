from rest_framework import status
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Sum
from customers.models import Customer
from payments.models import PaymentDetail
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


    def create(self, request):
        amount = request.data.get("amount")
        customer_external_id = request.data.get("customer")
        customer = Customer.objects.get(external_id_character=customer_external_id)
        
        loan_external_id = request.data.get("external_id_character")

        if customer.score >= amount:
            total_amount_dict = PaymentDetail.objects.filter(loan=loan_external_id).aggregate(total_amount=Sum('amount'))
            total_amount = total_amount_dict.get("total_amount")
            if total_amount:
                outstanding = amount - total_amount
            else:
                outstanding = amount - 0

            if outstanding <= 0:
                loan_status  = 4
            else:
                loan_status = request.data.get("status") or 1

            new_data = {
                "external_id_character": loan_external_id,
                "amount": amount,
                "maximum_payment_date": request.data.get("maximum_payment_date"),
                "taken_at": request.data.get("taken_at"),
                "outstanding": outstanding,
                "contract_version_character": request.data.get("contract_version_character"),
                "status": loan_status,
                "customer": customer.external_id_character
            }

            serializer = LoanSerializer(data=new_data)    
            if serializer.is_valid():
                serializer.save()
                customer.score = amount - float(customer.score)
                customer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)        
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"error": "Customer score should be greater than loan amount"}, status=status.HTTP_400_BAD_REQUEST)
