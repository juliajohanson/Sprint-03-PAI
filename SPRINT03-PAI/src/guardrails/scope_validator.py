class GuardrailException(Exception):
    """Exceção para violações de segurança ou escopo."""
    pass

TERMOS_BLOQUEADOS = ["instalação elétrica sem técnico", "bypass", "jailbreak", "hackear", "processo judicial"]

def validar_escopo_mensagem(mensagem: str) -> None:
    texto = mensagem.lower()
    for termo in TERMOS_BLOQUEADOS:
        if termo in texto:
            raise GuardrailException(
                "Solicitação bloqueada: Não é permitido fornecer instruções de segurança elétrica sem técnico habilitado ou atender fora do escopo estipulado."
            )