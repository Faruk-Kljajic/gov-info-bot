import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI

# Laden der Umgebungsvariablen
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path=dotenv_path)

# CSV-Daten laden
def get_csv_data():
    csv_path = os.path.join(os.getcwd(), "application/resources/wahldaten2024.csv")
    try:
        df = pd.read_csv(csv_path, encoding="ISO-8859-1", sep=";", on_bad_lines="skip")
    except FileNotFoundError:
        raise FileNotFoundError("CSV-Datei nicht gefunden.")
    return df

# LLM-Instanz erstellen
def get_llm_instance():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API-Key nicht gesetzt.")
    return ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o-mini", max_tokens=500, temperature=1, top_p=0.8)
