from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import BaseMessage
from langchain.chat_models.openai import ChatOpenAI
import tiktoken

def count_tokens(prompt: str, model: str = "gpt-4") -> int:
    tokenizer = tiktoken.encoding_for_model(model)
    return len(tokenizer.encode(prompt))

MAX_TOKENS = 4000  # Token-Limit für das Modell

def generate_response(llm: ChatOpenAI, prompt: str) -> str:
    """
    Generiert eine Antwort basierend auf einem gegebenen Prompt.

    :param llm: Die LLM-Instanz.
    :param prompt: Der Prompt für das Language Model.
    :return: Die generierte Antwort als String.
    """
    try:
        # Kürze den Prompt, falls er das Token-Limit überschreitet
        tokens = count_tokens(prompt, model='gpt-4')
        if tokens > MAX_TOKENS:
            prompt = " ".join(tokens[:MAX_TOKENS]) + "\n(Der Prompt wurde gekürzt.)"

        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Fehler bei der Generierung der Antwort: {e}"
