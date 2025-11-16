from typing import Mapping, Dict, Any


class InventoryCheckService:
    """
    Serviço stateless que verifica disponibilidade de SKUs em um snapshot de estoque.
    Snapshot esperado: mapping sku -> available_quantity (int)
    """

    def __init__(self):
        pass

    def check_availability(
        self, snapshot: Mapping[str, int], requested: Mapping[str, int]
    ) -> Dict[str, Any]:
        """
        Retorna:
          - available: bool (true se todos itens disponíveis)
          - details: mapping sku -> dict(requested, available, ok)
        Não altera snapshot (stateless).
        """
        details = {}
        all_ok = True
        for sku, qty in requested.items():
            if sku not in snapshot:
                available = 0
            else:
                available = int(snapshot[sku])
            ok = int(qty) <= available
            details[sku] = {"requested": int(qty), "available": available, "ok": ok}
            if not ok:
                all_ok = False
        return {"available": all_ok, "details": details}
