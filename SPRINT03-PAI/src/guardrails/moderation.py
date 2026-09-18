from src.guardrails.scope_validator import GuardrailException

PALAVRAS_RESERVADAS_MODERACAO = [
    "fazer gato", "ligar direto", "gambiarra", "curto circuito",
    "burlar medidor", "senha root", "prompt injection"
]

def verificar_moderacao(texto: str) -> None:
    """Valida se o texto contém violações de segurança elétrica ou jailbreak."""
    texto_lower = texto.lower()
    for termo in PALAVRAS_RESERVADAS_MODERACAO:
        if termo in texto_lower:
            raise GuardrailException(
                f"Moderação ativada: O termo '{termo}' viola as diretrizes de segurança da GoodWe."
            )