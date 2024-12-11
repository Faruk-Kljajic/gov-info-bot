from langchain.llms import OpenAI

# Initialisiere LLM
llm = OpenAI(model="gpt-4", temperature=0.7)

def generate_response_with_data(query, results):
    # Gefundene Daten kombinieren
    data_context = "\n".join([result.page_content for result in results])

    # Prompt erstellen
    prompt = f"""
    Benutzerfrage: {query}
    Basierend auf den gefundenen Informationen:
    {data_context}
    Erstelle eine präzise Antwort für den Benutzer.
    """
    return llm.generate(prompt).content
