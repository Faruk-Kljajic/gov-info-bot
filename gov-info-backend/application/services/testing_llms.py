from llm_client import create_llm_client  # Importiere die Factory-Funktion
from llm_service import LLMService


# Testaufruf
if __name__ == "__main__":
    # System- und Benutzernachricht definieren
    system_message = "Du bist ein hilfreicher Assistent."
    user_message = "Erkläre das Konzept von RAG."

    # LLM-Client erstellen (z. B. "openai" oder "huggingface")
    client_type = "openai"  # Ändere dies, um einen anderen LLM-Client zu verwenden
    llm_client = create_llm_client(client_type)

    # LLM-Service mit dem gewählten Client initialisieren
    llm_service = LLMService(llm_client=llm_client)

    # Benutzer-Prompt analysieren
    response = llm_service.analyze_prompt(system_message, user_message)

    # Antwort ausgeben
    print("Antwort des LLMs:", response)