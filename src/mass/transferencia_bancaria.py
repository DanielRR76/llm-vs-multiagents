from decimal import Decimal, ROUND_HALF_UP
import re


class TransferirUC:
    MIN_TRANSFER = Decimal("1.00")
    MAX_TRANSFER = Decimal("100000.00")

    EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")
    BLOCKED_DOMAINS = {"example.com", "test.com"}

    def validate_transfer(
        self, remetente, email_destino_raw: str, valor: Decimal
    ) -> str | None:
        email_destino = (
            None if email_destino_raw is None else email_destino_raw.strip().lower()
        )
        if remetente is None:
            return "Sessão expirada. Faça login novamente."

        if not email_destino:
            return "Informe o e-mail do destinatário."

        if not TransferirUC.EMAIL_RE.match(email_destino):
            return "E-mail do destinatário inválido."

        parts = email_destino.split("@", 1)
        domain = parts[1] if len(parts) == 2 else ""
        if domain in TransferirUC.BLOCKED_DOMAINS:
            return "Transferências para este domínio estão bloqueadas."

        if valor is None:
            return "Informe um valor numérico válido."

        if valor <= 0:
            return "Informe um valor maior que zero."
        valor = valor.normalize()
        try:
            exp = int(valor.as_tuple().exponent)
        except Exception:
            return "Informe um valor numérico válido."

        casas_decimais = -exp

        if casas_decimais > 2:
            return "Use no máximo duas casas decimais."

        valor = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if (
            remetente.email is not None
            and email_destino == remetente.email.strip().lower()
        ):
            return "Não é possível transferir para a própria conta."
        if valor < TransferirUC.MIN_TRANSFER:
            return "Valor mínimo por transferência é R$ 1.00."
        if valor > TransferirUC.MAX_TRANSFER:
            return "Valor máximo por transferência é R$100000.00."

        return None
