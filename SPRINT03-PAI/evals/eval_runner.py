import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import time
import tiktoken
from src.chain.builder import executar_chat

# Dataset herdado da Sprint 2
EVAL_SET = [
    "O que é o desafio ChargeGrid Intelligence da GoodWe?",
    "Quais são os modelos disponíveis na linha HCA G2?",
    "A linha HCA G2 possui suporte ao protocolo OCPP para cobranças?",
    "Existe alguma API disponível para integração ou monitoramento?",
    "Como funciona o modo Controle Dinâmico de Carga?"
]

def contar_tokens(texto: str) -> int:
    """Conta tokens utilizando a biblioteca tiktoken exigida na Sprint 03."""
    encoder = tiktoken.get_encoding("cl100k_base")
    return len(encoder.encode(texto))

def executar_bateria_evals():
    resultados = []
    print("Iniciando execução do Eval Set (Sprint 03)...")
    
    for idx, pergunta in enumerate(EVAL_SET, 1):
        inicio = time.time()
        resposta = executar_chat(pergunta, session_id=f"eval_session_{idx}")
        tempo_execucao = round(time.time() - inicio, 2)
        
        tokens_input = contar_tokens(pergunta)
        tokens_output = contar_tokens(resposta)
        
        resultados.append({
            "id": idx,
            "pergunta": pergunta,
            "resposta": resposta,
            "latencia_segundos": tempo_execucao,
            "tokens_input": tokens_input,
            "tokens_output": tokens_output,
            "status": "SUCESSO"
        })
        print(f"✅ Teste {idx}/{len(EVAL_SET)} concluído em {tempo_execucao}s")

    # Salva o arquivo de evidência JSON
    with open("evals/sprint3_results.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
        
    print("📄 Resultados salvos em 'evals/sprint3_results.json'")

if __name__ == "__main__":
    executar_bateria_evals()