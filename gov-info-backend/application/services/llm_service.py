from langchain.llms import OpenAI

def generate_response_with_data(query, results, max_context_length: int = 1000):
    # Gefundene Daten kombinieren
    data_context = "\n".join([result.page_content for result in results])

    # Kürze die Daten, falls sie zu lang sind
    if len(data_context) > max_context_length:
        data_context = data_context[:max_context_length] + "...\n(Daten gekürzt)"

    # Prompt erstellen
    prompt = f"""
    Benutzerfrage: {query}
    Basierend auf den gefundenen Informationen:
    {data_context}
    Erstelle eine präzise Antwort für den Benutzer.
    """
    return OpenAI(model="gpt-4", temperature=0.7).generate(prompt).content
