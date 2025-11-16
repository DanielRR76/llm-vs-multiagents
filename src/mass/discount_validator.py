from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Mapping, Any, Optional


class DiscountValidatorService:
    """
    Valida regras simples de desconto/cupom sem estado.
    Regras suportadas (cada cupom dikt é dict):
      - code: str
      - type: 'percentage' | 'fixed'
      - value: Decimal
      - min_subtotal: Decimal (opcional)
      - expires_at: ISO8601 string (opcional)
      - usage_limit: int (opcional)  <-- esta classe não acompanha usos, só valida payload
    """

    def __init__(self):
        pass

    def validate(
        self,
        coupon: Mapping[str, Any],
        subtotal: Decimal,
        now: Optional[datetime] = None,
    ) -> bool:
        if not isinstance(subtotal, Decimal):
            raise TypeError("subtotal must be Decimal")
        required = {"code", "type", "value"}
        if not required.issubset(set(coupon.keys())):
            raise ValueError("coupon missing required fields")
        ctype = coupon["type"]
        if ctype not in ("percentage", "fixed"):
            raise ValueError("unsupported coupon type")
        value = Decimal(str(coupon["value"]))
        if value < 0:
            raise ValueError("coupon value must be non-negative")
        if "min_subtotal" in coupon:
            min_sub = Decimal(str(coupon["min_subtotal"]))
            if subtotal < min_sub:
                return False
        if "expires_at" in coupon:
            now = now or datetime.now(timezone.utc)
            expires = datetime.fromisoformat(str(coupon["expires_at"]))
            if now > expires:
                return False
        # usage_limit is out of scope for stateless validator
        return True

    def apply(self, coupon: Mapping[str, Any], subtotal: Decimal) -> Decimal:
        """
        Retorna desconto (Decimal) para ser subtraído do subtotal.
        Não valida; espera que validate() seja chamada antes.
        """
        if not isinstance(subtotal, Decimal):
            raise TypeError("subtotal must be Decimal")
        ctype = coupon["type"]
        value = Decimal(str(coupon["value"]))
        if ctype == "percentage":
            discount = (subtotal * value).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            return discount
        else:
            return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
