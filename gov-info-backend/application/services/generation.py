from langchain_openai.chat_models import ChatOpenAI

def generate_response(llm: ChatOpenAI, prompt: str) -> str:
    """
    Generiert eine Antwort basierend auf einem gegebenen Prompt.

    :param llm: Die LLM-Instanz.
    :param prompt: Der Prompt für das Language Model.
    :return: Die generierte Antwort als String.
    """
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Fehler bei der Generierung der Antwort: {e}"
