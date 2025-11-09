# ecommerce_services.py
from decimal import Decimal
from typing import Mapping, Optional


class FraudScorerService:
    """
    Score de fraude determinístico e testável com heurísticas simples:
      - order_value (Decimal)
      - email_age_days (int)
      - ip_risk_score (0..1)
    Retorna score 0.0 (baixo risco) .. 1.0 (alto risco).
    """

    def __init__(self, weights: Optional[Mapping[str, float]] = None):
        # pesos aplicados a cada fator (soma não precisa ser 1)
        defaults = {"value_weight": 0.5, "email_age_weight": 0.3, "ip_weight": 0.2}
        self.weights = dict(weights or defaults)

    def score(self, order_value: Decimal, email_age_days: int, ip_risk_score: float) -> float:
        if not isinstance(order_value, Decimal):
            raise TypeError("order_value must be Decimal")
        if email_age_days < 0:
            raise ValueError("email_age_days must be >= 0")
        if not (0.0 <= ip_risk_score <= 1.0):
            raise ValueError("ip_risk_score must be in [0,1]")

        # normaliza order_value para [0,1] usando uma heurística: cap em 2000
        v = float(order_value)
        norm_value = min(v / 2000.0, 1.0)
        norm_email = 1.0 - min(email_age_days / 365.0, 1.0)  # contas novas = mais risco
        norm_ip = float(ip_risk_score)

        wv = self.weights.get("value_weight", 0.5)
        we = self.weights.get("email_age_weight", 0.3)
        wi = self.weights.get("ip_weight", 0.2)

        raw = (norm_value * wv) + (norm_email * we) + (norm_ip * wi)
        # normaliza para 0..1
        score = max(0.0, min(raw, 1.0))
        return float(round(score, 4))
