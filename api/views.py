from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema # type: ignore
from drf_yasg import openapi

from .serializers import CustomerSerializer, LoanSerializer, PaymentDetailSerializer, PaymentSerializer
from .models import Customer, Loan, Payment, PaymentDetail


class CustomerViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for create and get customers.
    """

    queryset = Customer.objects.all()
    serializer = CustomerSerializer(queryset, many=True)
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    customer_response = openapi.Response('response description', serializer_class.data)


    @swagger_auto_schema(responses = {200: customer_response})
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
        return Response({'status': 'password set'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
        auth = request.auth
        user = request.user
        data = request.data
        query_params = request.query_params
        return Response()


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
        auth = request.auth
        user = request.user
        data = request.data
        query_params = request.query_params
        return Response()