import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.schemas.consulta import ConsultaRecargaGoodWe
from src.chain.memoria import obter_historico_sessao
from src.guardrails.scope_validator import validar_escopo_mensagem

load_dotenv()
print("DEBUG - Host lido:", os.getenv("OLLAMA_HOST"))
print("DEBUG - Chave lida:", os.getenv("OLLAMA_API_KEY"))
# Instanciação do modelo LLM
llm = ChatOllama(
    model="gemma4:cloud",
    temperature=0.2,
    ollama_host=os.getenv("OLLAMA_HOST", "https://ollama.com"),
    client_kwargs={"headers": {"Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"}}
)

# Leitura do prompt versionado
with open("prompts/system_prompt_v1.md", "r", encoding="utf-8") as f:
    system_prompt_texto = f.read()

prompt_chat = ChatPromptTemplate.from_messages([
    ("system", system_prompt_texto),
    ("human", "{input}")
])

# Chain para conversação de chat
chat_runnable = prompt_chat | llm
chat_chain = RunnableWithMessageHistory(
    chat_runnable,
    get_session_history=obter_historico_sessao,
    input_messages_key="input",
    history_messages_key="history"
)

# Chain estruturada Pydantic v2
parser_pydantic = PydanticOutputParser(pydantic_object=ConsultaRecargaGoodWe)
prompt_estruturado = ChatPromptTemplate.from_template(
    system_prompt_texto + "\n\nResponda preenchendo a estrutura JSON:\n{format_instructions}\n\nPergunta: {pergunta}"
)

structured_chain = (
    prompt_estruturado.partial(format_instructions=parser_pydantic.get_format_instructions())
    | llm
    | parser_pydantic
)

def executar_chat(mensagem: str, session_id: str = "default_session") -> str:
    validar_escopo_mensagem(mensagem)
    resposta = chat_chain.invoke(
        {"input": mensagem},
        config={"configurable": {"session_id": session_id}}
    )
    return resposta.content

def executar_analise_estruturada(pergunta: str) -> ConsultaRecargaGoodWe:
    validar_escopo_mensagem(pergunta)
    return structured_chain.invoke({"pergunta": pergunta})