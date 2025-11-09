# ecommerce_services.py
import hashlib
from datetime import datetime
from typing import Optional


class OrderIdGeneratorService:
    """
    Gera um ID de pedido determinístico a partir de dados de pedido (por ex. user_id, timestamp, nonce).
    Usa SHA256 e retorna hex digest reduzido (por exemplo 16 chars) para legibilidade.
    """

    def __init__(self, namespace: Optional[str] = None):
        self.namespace = namespace or "ecom"

    def generate(self, user_id: str, timestamp: Optional[datetime] = None, nonce: Optional[str] = None) -> str:
        timestamp = timestamp or datetime.utcnow()
        nonce = nonce or ""
        payload = f"{self.namespace}|{user_id}|{timestamp.isoformat()}|{nonce}"
        h = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return h[:32]