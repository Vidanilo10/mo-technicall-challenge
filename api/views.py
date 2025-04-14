from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import CustomerSerializer, LoanSerializer, PaymentDetailSerializer, PaymentSerializer
from .models import Customer, Loan, Payment, PaymentDetail


"""
class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
"""


class CustomerViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving customers.
    """

    def list(self, request):
        queryset = Customer.objects.all()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request):
        dir_request = dir(request)
        return dir_request