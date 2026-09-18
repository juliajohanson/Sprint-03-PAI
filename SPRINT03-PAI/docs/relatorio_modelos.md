# Relatório de Uso de Modelos e Parâmetros - Sprint 03

Este documento compara a performance e os parâmetros de dois modelos testados para o núcleo conversacional do ChargeGrid GoodWe.

## 1. Comparativo de Modelos

| Critério | Modelo A (Principal) | Modelo B (Comparativo) |
| :--- | :--- | :--- |
| **Nome do Modelo** | `llama3.2:1b` (Local) | `gemma4:cloud` (Nuvem) / `gpt-4o-mini` |
| **Tempo de Resposta (Latência)** | ~3.5 segundos | ~1.2 segundos |
| **Acurácia Pydantic v2** | 90% (alguns erros de formatação) | 100% de aderência ao JSON |
| **Compreensão de Contexto** | Boa, mas exige prompts mais diretos | Excelente retenção de memória |

## 2. Configuração de Hiperparâmetros

Os seguintes parâmetros foram fixados na chamada (`llm = Chat...`) para garantir consistência:

* **`temperature` (0.2):** Reduzida drasticamente em relação ao padrão (0.7/0.8) para evitar alucinações técnicas e garantir respostas focadas nas especificações rígidas da linha HCA G2.
* **`top_p` (0.9):** Mantém a diversidade do vocabulário contida dentro de termos técnicos de alta probabilidade.
* **`max_tokens` (500):** Limite estabelecido para evitar respostas excessivamente longas e economizar custos de API/processamento.