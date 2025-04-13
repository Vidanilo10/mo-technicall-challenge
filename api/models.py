from django.db import models

class Customer(models.Model):
    created_timestamp = models.DateTimeField()
    updated_timestamp = models.DateTimeField()
    external_id_character = models.IntegerField()
    score = models.DecimalField()
    preapproved_at = models.DateTimeField()

    class CustomerStatus(models.IntegerChoices):
        ACTIVE = 1, "Active"
        INACTIVE = 2, "Inactive"

    status = models.IntegerField(
        choices=CustomerStatus.choices,
        default=CustomerStatus.ACTIVE,
        verbose_name="Estado"
    )

    def __str__(self):
        return self.status


class Loan(models.Model):
    created_timestamp = models.DateTimeField()
    updated_timestamp = models.DateTimeField()
    external_id_character = models.IntegerField()
    amount = models.DecimalField()
    contract_version_character = models.CharField(max_length=30)
    maximum_payment_date = models.DateTimeField()
    taken_at = models.DateTimeField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    outstanding = models.IntegerField()

    class LoanStatus(models.IntegerChoices):
        PENDING = 1, "Active"
        ACTIVE = 2, "Inactive"
        REJECTED = 3, "Rejected"
        PAID = 4, "Paid"

    status = models.IntegerField(
        choices=LoanStatus.choices,
        default=LoanStatus.PENDING,
        verbose_name="Estado"
    )


    def __str__(self):
        return self.contract_version_character




class Payment(models.Model):
    created_timestamp = models.DateTimeField()
    updated_timestamp = models.DateTimeField()
    external_id_character = models.CharField(max_length=60)
    total_amount = models.DecimalField()
    paid_at = models.DateTimeField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class PaymentStatus(models.IntegerChoices):
        COMPLETED = 1, "Completed"
        REJECTED = 2, "Rejected"

    status = models.IntegerField(
        choices=PaymentStatus.choices,
        verbose_name="Estado"
    )


    def __str__(self):
        return self.status



class PaymentDetail(models.Model):
    created_timestamp = models.DateTimeField()
    updated_timestamp = models.DateTimeField()
    amount = models.DecimalField()
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
