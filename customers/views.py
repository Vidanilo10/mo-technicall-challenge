from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema # type: ignore
from drf_yasg import openapi

from django.db.models import Sum

from .serializers import CustomerSerializer
from .models import Customer
from loans.models import Loan


class CustomerViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for create and get customers.
    """

    queryset = Customer.objects.all()
    serializer = CustomerSerializer(queryset, many=True)
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    customer_response = openapi.Response('response description', serializer_class)

    def list(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializer_class, responses = {201: customer_response})
    def create(self, request):
        serializer = CustomerSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=True, methods=['get'])
    def get_customer_balance(self, request, pk=None):

        customer = Customer.objects.get(pk=pk)
        score = customer.score
        total_debt = Loan.objects.filter(external_id_character=pk).aggregate(total_amount=Sum('outstanding'))
        
        total_debt_value = total_debt.get("total_amount")

        if not total_debt_value:
            total_debt_value = float(0.0)
        else:
            if total_debt_value != 0.0 and total_debt_value != float(0):
                total_debt_value = float(total_debt_value)
            else:
                total_debt_value = float(0.0)

        available_amount = float(score) - total_debt_value
        
        return_data = {
            "external_id": customer.external_id_character,
            "score": score,
            "available_amount": available_amount,
            "total_debt": total_debt_value
        }
        
        return Response(return_data, status=status.HTTP_200_OK)
