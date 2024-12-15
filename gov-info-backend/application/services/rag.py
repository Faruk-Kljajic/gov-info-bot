from application.services.retrieval import filter_data
from application.services.generation import generate_response, count_tokens, MAX_TOKENS
from langchain_openai.chat_models import ChatOpenAI
from typing import Optional

import pandas as pd

def process_query(df: pd.DataFrame, llm: ChatOpenAI, frage: str, gebiet: Optional[str], partei: Optional[str]) -> str:
    """
    Orchestriert die Retrieval-Augmented Generation (RAG) Pipeline.

    :param df: Der DataFrame mit den Wahldaten.
    :param llm: Die LLM-Instanz.
    :param frage: Die Benutzerfrage.
    :param gebiet: Das zu filternde Gebiet.
    :param partei: Die zu filternde Partei.
    :return: Die generierte Antwort.
    """
    # Schritt 1: Daten filtern
    daten = filter_data(df, gebiet, partei)

    # Wenn keine passenden Daten gefunden wurden
    if "Keine passenden Daten gefunden" in daten or "Die Partei" in daten:
        prompt = (
            f"Der Benutzer hat nach '{frage}' gefragt, aber keine passenden Wahldaten wurden gefunden. "
            "Bitte gib eine allgemeine Antwort oder Tipps zur Fragestellung."
        )
        return generate_response(llm, prompt)

    # Schritt 2: Antwort basierend auf den Daten generieren
    prompt = f"{frage}\nHier sind die relevanten Wahldaten:\n{daten}\nBitte beantworte die Frage basierend auf den obigen Daten."

    # Kürze den Prompt, falls erforderlich
    tokens = count_tokens(prompt)
    if tokens > MAX_TOKENS:
        prompt = " ".join(tokens[:MAX_TOKENS]) + "\n(Der Prompt wurde gekürzt.)"

    return generate_response(llm, prompt)