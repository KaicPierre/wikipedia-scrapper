import os
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from app.settings import settings

from langchain_ollama import ChatOllama

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


class Summarizer(): 
  def summarize(self, data: str, word_count: int) -> str:
    
    if(settings.MODEL == "OLLAMA"):
      model = ChatOllama(model="llama3.2", temperature=0)
    else:
      model = init_chat_model(model="gpt-4.1")
    
    system_msg = SystemMessage(
        "Você é um assistente especializado em criar resumos concisos e precisos de artigos da Wikipedia. "
        "Suas respostas devem ser em texto corrido, sem formatação markdown, listas ou marcadores. "
        "Mantenha a objetividade e inclua apenas as informações mais relevantes. "
        "Respeite estritamente o limite de palavras especificado pelo usuário."
    )
    human_msg = HumanMessage(
        f"Crie um resumo do seguinte artigo da Wikipedia em exatamente {word_count} palavras ou menos. "
        f"Foque nos pontos principais e mantenha a clareza.\n\n"
        f"Conteúdo do artigo:\n{data}"
    )
    
    messages= [ system_msg, human_msg ]
    summary = model.invoke(messages)
    
    return summary.content