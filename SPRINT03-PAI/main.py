import gradio as gr
from src.chain.builder import executar_chat, executar_analise_estruturada
from src.guardrails.scope_validator import GuardrailException

def interacao_chat(mensagem, historico):
    try:
        return executar_chat(mensagem)
    except GuardrailException as ge:
        return f" **Alerta de Segurança:** {str(ge)}"
    except Exception as e:
        return f"Erro no processamento: {str(e)}"

def interacao_analise(pergunta):
    if not pergunta.strip():
        return "Por favor, insira uma consulta sobre os carregadores GoodWe."
    try:
        res = executar_analise_estruturada(pergunta)
        return (
            f"**Modelo Identificado:** {res.modelo_carregador}\n\n"
            f"**Potência:** {res.potencia_kw} kW\n\n"
            f"**Suporta OCPP:** {'Sim' if res.suporta_ocpp else 'Não'}\n\n"
            f"**Análise Técnica:**\n{res.explicacao_tecnica}"
        )
    except GuardrailException as ge:
        return f" **Solicitação Recusada:** {str(ge)}"
    except Exception as e:
        return f"Erro na validação Pydantic v2: {str(e)}"

with gr.Blocks(title="ChargeGrid GoodWe Assistant") as app:
    gr.Markdown("#  Assistente Técnico ChargeGrid - GoodWe")
    gr.Markdown("Consultas sobre carregadores veiculares da Linha HCA G2.")
    
    with gr.Tab("Chat de Atendimento"):
        gr.ChatInterface(fn=interacao_chat)
        
    with gr.Tab("Análise Estruturada (Pydantic v2)"):
        input_pergunta = gr.Textbox(label="Consulta Técnica", placeholder="Ex: Qual a potência do modelo GW11K-HCA-20 e se aceita OCPP?")
        btn_analisar = gr.Button("Analisar Especificações")
        output_analise = gr.Markdown(label="Relatório Técnico")
        
        btn_analisar.click(fn=interacao_analise, inputs=[input_pergunta], outputs=[output_analise])

if __name__ == "__main__":
    app.launch(server_port=7860)