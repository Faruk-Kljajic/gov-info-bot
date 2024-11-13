from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd
import re
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI

dotenv_path = os.path.join(os.getcwd(), 'app/routes/.env')
load_dotenv(dotenv_path=dotenv_path)
openai_api_key = os.getenv("OPENAI_API_KEY")

csv_path = os.path.join(os.getcwd(), 'app/ressources/wahldaten2024.csv')

try:
    df = pd.read_csv(csv_path, encoding='ISO-8859-1', sep=";", on_bad_lines='skip')
    print("CSV-Datei erfolgreich geladen!")
except Exception as e:
    print(f"Fehler beim Laden der Datei: {e}")
    df = pd.DataFrame()

llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o-mini", max_tokens=500)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.get("/")
async def read_root():
    return {"message": "Hello, Chatbot Backend is running!"}


@app.post("/chat/")
async def chat_response(message: Message):
    print("Empfangene Nachricht im Backend:", message.message)  # Debugging
    response = frage_chatbot(message.message)
    return {"response": response}

def extract_gebiet_und_partei(frage):
    gebiet = None
    partei = None
    partei_match = re.search(r"(ÖVP|SPÖ|FPÖ|GRÜNE|NEOS|BIER|MFG|BGE|LMP|GAZA|KPÖ|KEINE)", frage, re.IGNORECASE)
    if partei_match:
        partei = partei_match.group(1).strip()
    gebiet_match = re.search(r"(in|für)\s([A-Za-z\s]+)", frage)
    if gebiet_match:
        gebiet = gebiet_match.group(2).strip()
    return gebiet, partei

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
    return gefilterte_daten.to_string(index=False)

def frage_chatbot(frage):
    gebiet, partei = extract_gebiet_und_partei(frage)
    if gebiet or partei:
        daten = get_results_for_criteria(gebiet, partei)
        if "Keine passenden Daten gefunden" in daten or "Die Partei" in daten:
            return daten
        prompt = f"{frage}\nHier sind die relevanten Wahldaten:\n{daten}\nBitte beantworte die Frage basierend auf den obigen Daten."
        antwort = llm.invoke(prompt).content
    else:
        antwort = "Bitte geben Sie ein gültiges Gebiet oder eine Partei an."
    return antwort

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
