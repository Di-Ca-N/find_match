from typing import Protocol, TypedDict, NotRequired
from decimal import Decimal

class PaymentResponse(TypedDict):
    status: str
    amount: Decimal
    error: NotRequired[str]


class PaymentMethod(Protocol):
    def pay(self, amount: Decimal) -> PaymentResponse:
        raise NotImplementedError


class DummyPaymentMethod(PaymentMethod):
    """Dummy payment method. Only approves payments up to R$100,00"""

    def pay(self, amount: Decimal) -> PaymentResponse:
        if amount <= 100:
            return {
                "status": "success",
                "amount": amount
            }
        else:
            return {
                "status": "error",
                "amount": amount,
                "error": "Pagamento acima do valor permitido"
            }
