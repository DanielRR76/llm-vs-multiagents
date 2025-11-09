from decimal import Decimal
from datetime import time

class SaqueUC:

    @staticmethod
    def validar_saque(user_id: int, valor: Decimal, agora, account_dao):
        bloqueio_inicio1 = time(12, 0)
        bloqueio_fim1    = time(12, 30)
        bloqueio_inicio2 = time(18, 0)
        bloqueio_fim2    = time(18, 30)

        conta = account_dao.get_by_user_id(user_id)

        if conta is None:
            return "Erro: conta inválida ou inativa."

        # 12:00 - 12:30
        if not (agora < bloqueio_inicio1 or agora > bloqueio_fim1):
            return "Saque não permitido entre 12:00 e 12:30."

        # 18:00 - 18:30
        if not (agora < bloqueio_inicio2 or agora > bloqueio_fim2):
            return "Saque não permitido entre 18:00 e 18:30."

        if valor < Decimal("10"):
            return "Erro: valor menor que o saque mínimo."

        if valor > Decimal("2000"):
            return "Erro: valor maior que o saque máximo."

        if valor % Decimal("10") != Decimal("0"):
            return "Erro: valor deve ser múltiplo de 10."

        if conta.balance < valor:
            return "Erro: saldo insuficiente."

        return None