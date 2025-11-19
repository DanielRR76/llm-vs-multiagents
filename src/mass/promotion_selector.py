from decimal import Decimal, ROUND_HALF_UP
from typing import Sequence, Mapping, Dict, Any


class PromotionSelectorService:
    """
    Seleciona a melhor promoção aplicável entre uma lista fornecida.
    Promo formato (cada promo dict):
      - 'id': str
      - 'type': 'percentage' | 'fixed'
      - 'value': Decimal
      - 'min_subtotal': Decimal (optional)
      - 'combinable': bool (optional, default False)  <-- esta classe escolhe apenas uma promoção
    Retorna a promoção escolhida (ou None) e o valor do desconto.
    """

    def __init__(self):
        pass

    def select_best(
        self, promotions: Sequence[Mapping[str, Any]], subtotal: Decimal
    ) -> Dict[str, Any]:
        best = None
        best_discount = Decimal("0.00")
        for promo in promotions:
            if "type" not in promo or "value" not in promo:
                continue
            if "min_subtotal" in promo:
                min_sub = Decimal(str(promo["min_subtotal"]))
                if subtotal < min_sub:
                    continue
            ptype = promo["type"]
            value = Decimal(str(promo["value"]))
            if ptype == "percentage":
                discount = (subtotal * value).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            else:
                discount = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if discount > best_discount:
                best_discount = discount
                best = promo
        return {"promotion": best, "discount": best_discount}
