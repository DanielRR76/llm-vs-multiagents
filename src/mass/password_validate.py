import re


def validar_senha(senha: str) -> tuple[bool, str | None]:
    """
    retorna (validou, msgErro)
    """
    if not isinstance(senha, str):
        return False, "Senha deve ser uma string."

    if len(senha) < 8:
        return False, "Senha deve ter pelo menos 8 caracteres."

    if len(senha) > 30:
        return False, "Senha não deve ultrapassar 30 caracteres."

    if not re.search(r"\d", senha):
        return False, "Senha deve conter pelo menos um número."

    if not re.search(r"[A-Z]", senha):
        return False, "Senha deve conter pelo menos uma letra maiúscula."

    if not re.search(r"[a-z]", senha):
        return False, "Senha deve conter pelo menos uma letra minúscula."

    if not re.search(r"[!@#$%^&*()_+\-={}\[\]|:;\"'<>,.?/]", senha):
        return False, "Senha deve conter pelo menos um caractere especial."

    if " " in senha:
        return False, "Senha não deve conter espaços."

    if re.search(r"(.)\1\1", senha):
        return False, "Senha não deve conter três caracteres idênticos seguidos."

    lower = senha.lower()
    if "senha" in lower or "password" in lower:
        return (
            False,
            "Senha não deve conter palavras óbvias como 'senha' ou 'password'.",
        )

    return True, None
