from langchain_openai.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
import re
from ..services.data_handler import get_results_for_region


dotenv_path = os.path.join(os.getcwd(), 'app/routes/.env')
load_dotenv(dotenv_path=dotenv_path)
# Laden der Umgebungsvariablen aus der .env-Datei
# API-Schlüssel aus der Umgebung holen
#load_dotenv(dotenv_path='gov-info-backend/app/routes/.env')
openai_api_key = os.getenv("OPENAI_API_KEY")



# Initialisiere das Chat-Modell mit dem neuen Paket
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
        # Die Frage und die Ergebnisse aus der CSV in den LLM prompten
        prompt = f"{frage}\nHier sind die Wahldaten:\n{daten}"
        antwort = llm.invoke(prompt).content
    else:
        antwort = "Bitte geben Sie ein gültiges Gebiet an."

    return antwort

# Beispiel
frage = "Was sind die Nationalratswahlergebnisse 2024 für Linz?"
antwort = frage_chatbot(frage)
print("Frage vom User:",frage,"\nAntwort des Chatbots:\n", antwort)