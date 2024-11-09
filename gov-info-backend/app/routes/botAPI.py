from langchain_openai.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
import re
from app.services.data_handler import get_results_for_region

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# API-Schlüssel
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o-mini", max_tokens=500, temperature=1, top_p=0.8)

# Funktion, um den Gebietsnamen aus der Frage zu extrahieren
def extract_gebiet(frage):
    match = re.search(r"für\s([A-Za-z\s]+)", frage)
    return match.group(1) if match else None

# Hauptfunktion für den Chatbot
def frage_chatbot(frage):
    gebiet = extract_gebiet(frage)
    if gebiet:
        daten = get_results_for_region(gebiet)
        # Frage und Ergebnisse aus der CSV in den LLM prompten
        prompt = f"{frage}\nHier sind die Wahldaten:\n{daten}"
        antwort = llm.invoke(prompt).content
    else:
        antwort = "Bitte geben Sie ein gültiges Gebiet an."

    return antwort

# Beispiel
frage = "Was sind die Nationalratswahlergebnisse 2024 für Linz?"
antwort = frage_chatbot(frage)
print("Frage vom User:",frage,"\nAntwort des Chatbots:\n", antwort)