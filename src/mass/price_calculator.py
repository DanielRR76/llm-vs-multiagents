from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Sequence, Mapping, Dict, Any

# Aumenta precisão decimal para cálculos monetários
getcontext().prec = 12


class PriceCalculatorService:
    """
    Serviço stateless para calcular preços de um pedido.
    Entrada: lista de itens (unit_price, quantity), shipping_cost (Decimal) opcional,
    tax_rate (Decimal) opcional (se não informado, 0).
    Retorna dict com subtotal, tax, total (Decimal com 2 casas).
    """

    def __init__(self):
        pass

    def calculate(self,
                  items: Sequence[Mapping[str, Any]],
                  shipping_cost: Decimal = Decimal("0.00"),
                  tax_rate: Decimal = Decimal("0.00"),
                  rounding: str = "0.01") -> Dict[str, Decimal]:
        """
        items: sequência de dicionários com keys: 'unit_price' (Decimal/float/int/str), 'quantity' (int)
        tax_rate: Decimal (por ex. Decimal('0.10') para 10%)
        shipping_cost: Decimal
        """
        if not isinstance(shipping_cost, Decimal):
            raise TypeError("shipping_cost must be Decimal")
        if not isinstance(tax_rate, Decimal):
            raise TypeError("tax_rate must be Decimal")

        subtotal = Decimal("0.00")
        for idx, it in enumerate(items):
            if "unit_price" not in it or "quantity" not in it:
                raise ValueError(f"item[{idx}] missing unit_price or quantity")
            price = Decimal(str(it["unit_price"]))
            qty = int(it["quantity"])
            if price < 0 or qty < 0:
                raise ValueError("unit_price and quantity must be non-negative")
            subtotal += (price * Decimal(qty))

        subtotal = subtotal.quantize(Decimal(rounding), rounding=ROUND_HALF_UP)
        tax = (subtotal * tax_rate).quantize(Decimal(rounding), rounding=ROUND_HALF_UP)
        total = (subtotal + tax + shipping_cost).quantize(Decimal(rounding), rounding=ROUND_HALF_UP)

        return {"subtotal": subtotal, "tax": tax, "shipping": shipping_cost, "total": total}
