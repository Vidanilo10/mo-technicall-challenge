from django.db import models

class Customer(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    external_id_character = models.CharField(max_length=60)
    score = models.DecimalField(decimal_places=2, max_digits=10)
    preapproved_at = models.DateTimeField()

    class CustomerStatus(models.IntegerChoices):
        ACTIVE = 1, "Active"
        INACTIVE = 2, "Inactive"

    status = models.IntegerField(
        choices=CustomerStatus.choices,
        default=CustomerStatus.ACTIVE,
        verbose_name="Estado"
    )
