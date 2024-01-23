from django.db import models

from decimal import Decimal
import random
import requests
import string

from .payment_methods import PaymentMethod


class PaymentStatus(models.TextChoices):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    WITH_ERROR = "Error"

def random_code() -> str:
    return "".join(random.choices(string.ascii_letters, k=10))


class Payment(models.Model):
    code = models.CharField(max_length=10, default=random_code)
    value = models.DecimalField(decimal_places=2, max_digits=6)
    status = models.CharField(max_length=10, choices=PaymentStatus.choices)
    error_message = models.CharField(max_length=100)

    def pay(self, paymentMethod: PaymentMethod):
        if self.status != PaymentStatus.PENDING:
            raise ValueError(f"Cannot pay Payment with status {self.status}")

        response = paymentMethod.pay(self.value)

        match response:
            case {"status": "success"}:
                self.status = PaymentStatus.CONFIRMED
            case {"status": "error", "error": msg}:
                self.status = PaymentStatus.WITH_ERROR
                self.error_message = msg
        self.save()
    
    def is_confirmed(self):
        return self.status == PaymentStatus.CONFIRMED
