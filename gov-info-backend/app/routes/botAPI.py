from langchain_openai.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
import re

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# API-Schlüssel aus der Umgebung holen
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialisiere das Chat-Modell mit dem neuen Paket
llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o-mini", max_tokens=500, temperature=0.4, top_p=0.8)


# Funktion, um den Gebietsnamen aus der Frage zu extrahieren
def extract_gebiet(frage):
    match = re.search(r"für\s([A-Za-z\s]+)\?", frage)
    return match.group(1) if match else None


# Funktion, um eine einfache Frage an den Chatbot zu stellen
def frage_chatbot(frage):
    # Gebiet aus der Frage extrahieren
    gebiet = extract_gebiet(frage)

    # SQL-Abfrage nur ausführen, wenn ein Gebiet gefunden wurde
    if gebiet:
        query = f"SELECT * FROM wahlergebnisse WHERE Gebietsname = '{gebiet}'"
        #db_data = get_data_from_db(query)

        # Formatiere die Daten aus der Datenbank für das Prompt
        #db_data_str = "\n".join([str(row) for row in db_data])
        #prompt = f"{frage}\n\nDaten aus der Datenbank:\n{db_data_str}"
    else:
        prompt = frage  # Falls kein Gebiet gefunden wurde, verwende nur die Frage als Prompt

    antwort = llm.invoke(prompt)
    return antwort


# Beispielanfrage
frage = "Was sind die Nationalratswahl 2024 für Wien?"
antwort = frage_chatbot(frage)
print("Antwort des Chatbots:", antwort)
