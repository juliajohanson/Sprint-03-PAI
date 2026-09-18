from langchain_core.chat_history import InMemoryChatMessageHistory

# Dicionário global para armazenar o histórico por ID de sessão
armazenamento_sessoes = {}

def obter_historico_sessao(session_id: str) -> InMemoryChatMessageHistory:
    
    if session_id not in armazenamento_sessoes:
        armazenamento_sessoes[session_id] = InMemoryChatMessageHistory()
    return armazenamento_sessoes[session_id]