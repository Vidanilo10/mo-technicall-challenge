from django.db import models

# Create your models here.

class Customer(models.Model):
    created_timestamp = models.DateTimeField()
    updated_timestamp = models.DateTimeField()
    external_id_character = models.IntegerField()
    status = models.CharField(max_length=10)
    score = models.IntegerField()
    preapproved_at = models.DateTimeField()


class Loan(models.Model):
    created_timestamp = models.DateTimeField()
    updated_timestamp = models.DateTimeField()
    external_id_character = models.IntegerField()
    amount = models.IntegerField()
    status = models.CharField(max_length=10)
    contract_version_character = models.CharField(max_length=30)
    maximum_payment_date = models.DateTimeField()
    taken_at = models.DateTimeField()
    customer_id = models.IntegerField()
    outstanding = models.IntegerField()


class Payment(models.Model):
    created_timestamp = models.DateTimeField()
    updated_timestamp = models.DateTimeField()
    external_id_character = models.IntegerField()
    total_amount = models.IntegerField()
    status = models.CharField(max_length=10)
    paid_at = models.DateTimeField()
    customer_id = models.IntegerField()
