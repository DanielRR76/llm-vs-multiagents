
# ecommerce_services.py
import math
from decimal import Decimal, ROUND_HALF_UP
from typing import Mapping, Dict, Any, Optional, Tuple


class ShippingEstimatorService:
    """
    Estima distância (km) e custo de frete com base em:
      - peso total (kg)
      - origem (lat, lon) e destino (lat, lon)
      - speed_factor: 'standard'|'express'|'economy'
      - price factors: base_per_km (Decimal), per_kg (Decimal), speed_multiplier map
    Stateless e determinístico.
    """

    EARTH_RADIUS_KM = 6371.0

    def __init__(self, base_per_km: Decimal = Decimal("0.50"), per_kg: Decimal = Decimal("0.10"),
                 speed_multipliers: Optional[Mapping[str, Decimal]] = None):
        if not isinstance(base_per_km, Decimal) or not isinstance(per_kg, Decimal):
            raise TypeError("rates must be Decimal")
        self.base_per_km = base_per_km
        self.per_kg = per_kg
        self.speed_multipliers = dict(speed_multipliers or {
            "economy": Decimal("0.8"),
            "standard": Decimal("1.0"),
            "express": Decimal("1.5")
        })

    def _haversine_km(self, origin: Tuple[float, float], destination: Tuple[float, float]) -> float:
        lat1, lon1 = origin
        lat2, lon2 = destination
        φ1 = math.radians(lat1)
        φ2 = math.radians(lat2)
        Δφ = math.radians(lat2 - lat1)
        Δλ = math.radians(lon2 - lon1)
        a = math.sin(Δφ / 2) ** 2 + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        km = self.EARTH_RADIUS_KM * c
        return km

    def estimate(self, origin: Tuple[float, float], destination: Tuple[float, float],
                 weight_kg: float, speed: str = "standard") -> Dict[str, Any]:
        if speed not in self.speed_multipliers:
            raise ValueError("unknown speed")
        if weight_kg < 0:
            raise ValueError("weight_kg must be non-negative")
        km = Decimal(str(self._haversine_km(origin, destination))).quantize(Decimal("0.01"))
        base_cost = (self.base_per_km * km).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        weight_cost = (self.per_kg * Decimal(str(weight_kg))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        multiplier = self.speed_multipliers[speed]
        total = ((base_cost + weight_cost) * multiplier).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return {"distance_km": float(km), "base_cost": base_cost, "weight_cost": weight_cost, "speed": speed,
                "multiplier": multiplier, "total": total}
