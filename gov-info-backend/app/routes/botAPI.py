from langchain_openai.chat_models import ChatOpenAI
import os
import pandas as pd
import re
from dotenv import load_dotenv

# Lade die Umgebungsvariablen
dotenv_path = os.path.join(os.getcwd(), 'app/routes/.env')
load_dotenv(dotenv_path=dotenv_path)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Setze den vollständigen Pfad zur CSV-Datei und versuche die Datei zu laden
csv_path = os.path.join(os.getcwd(), 'app/ressources/wahldaten2024.csv')

try:
    # CSV-Datei laden mit Kodierung und Fehlerbehandlung
    df = pd.read_csv(csv_path, encoding='ISO-8859-1', sep=";", on_bad_lines='skip')
    print("CSV-Datei erfolgreich geladen!")
except FileNotFoundError:
    print("CSV-Datei nicht gefunden. Bitte den Pfad überprüfen.")
    df = pd.DataFrame()  # Leerer DataFrame, falls Datei nicht geladen werden kann
except pd.errors.ParserError as e:
    print(f"Fehler beim Laden der Datei: {e}")
except Exception as e:
    print(f"Ein unbekannter Fehler ist aufgetreten: {e}")
    df = pd.DataFrame()

# Initialisiere das ChatGPT-Modell
llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o-mini", max_tokens=500, temperature=1, top_p=0.8)


# Funktion zum Extrahieren des Gebiets oder der Partei aus der Frage
def extract_gebiet_und_partei(frage):
    print(f"Extrahiere Gebiet und Partei aus der Frage: {frage}")  # Debugging
    gebiet = None
    partei = None

    # Partei extrahieren (z.B., SPÖ, ÖVP, FPÖ, etc.)
    partei_match = re.search(r"(ÖVP|SPÖ|FPÖ|GRÜNE|NEOS|BIER|MFG|BGE|LMP|GAZA|KPÖ|KEINE)", frage, re.IGNORECASE)
    if partei_match:
        partei = partei_match.group(1).strip()
        print(f"Extrahierte Partei: {partei}")  # Debugging

    # Optional: Gebiet extrahieren, falls vorhanden
    gebiet_match = re.search(r"(in|für)\s([A-Za-z\s]+)", frage)
    if gebiet_match:
        gebiet = gebiet_match.group(2).strip()
        print(f"Extrahiertes Gebiet: {gebiet}")  # Debugging

    return gebiet, partei


# Funktion, um Ergebnisse für eine Partei oder ein Gebiet zu erhalten
def get_results_for_criteria(gebiet, partei):
    if df.empty:
        return "Die Wahldaten konnten nicht geladen werden."

    gefilterte_daten = df

    if gebiet:
        gefilterte_daten = gefilterte_daten[gefilterte_daten['Gebietsname'].str.contains(gebiet, case=False, na=False)]
    if partei and partei in gefilterte_daten.columns:
        gefilterte_daten = gefilterte_daten[['Gebietsname', partei]]
    elif partei:
        return f"Die Partei '{partei}' wurde in den Daten nicht gefunden."

    if gefilterte_daten.empty:
        return "Keine passenden Daten gefunden."

    daten_text = gefilterte_daten.to_string(index=False)
    return daten_text


# Hauptfunktion für den Chatbot
def frage_chatbot(frage):
    print(f"Empfangene Frage: {frage}")  # Debugging
    gebiet, partei = extract_gebiet_und_partei(frage)

    if gebiet or partei:
        daten = get_results_for_criteria(gebiet, partei)
        if "Keine passenden Daten gefunden" in daten or "Die Partei" in daten:
            return daten

        # Erstelle den Prompt mit der Frage und den gefilterten Daten
        prompt = f"{frage}\nHier sind die relevanten Wahldaten:\n{daten}\nBitte beantworte die Frage basierend auf den obigen Daten."
        antwort = llm.invoke(prompt).content
    else:
        antwort = "Bitte geben Sie ein gültiges Gebiet oder eine Partei an."

    print(f"Antwort des Chatbots: {antwort}")  # Debugging
    return antwort


# Beispiel-Frage
frage = "Wo hat die SPÖ die meisten Stimmen erhalten?"
antwort = frage_chatbot(frage)
print("Frage vom User:", frage, "\nAntwort des Chatbots:\n", antwort)
