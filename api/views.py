from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CustomerSerializer, LoanSerializer, PaymentDetailSerializer, PaymentSerializer
from .models import Customer, Loan, Payment, PaymentDetail


class CustomerViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for create and get customers.
    """

    queryset = Customer.objects.all()
    serializer = CustomerSerializer(queryset, many=True)
    serializer_class = CustomerSerializer

    def list(self, request):
        return Response(self.serializer.data)


    def create(self, request):
        auth = request.auth
        user = request.user
        data = request.data
        query_params = request.query_params
        return Response()
    

    @action(detail=True, methods=['get'])
    def get_customer_balance(self, request, pk=None):
        return Response({'status': 'password set'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoansViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for create and query loan by customer.
    """

    queryset = Loan.objects.all()
    serializer = LoanSerializer(queryset, many=True)
    serializer_class = LoanSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer']


    def create(self, request):
        auth = request.auth
        user = request.user
        data = request.data
        query_params = request.query_params
        return Response()


class PaymentsViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for create and query payment by customer.
    """

    queryset = Payment.objects.all()
    serializer = PaymentSerializer(queryset, many=True)
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer']

    def create(self, request):
        auth = request.auth
        user = request.user
        data = request.data
        query_params = request.query_params
        return Response()
