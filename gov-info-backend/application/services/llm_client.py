from abc import ABC, abstractmethod
from typing import Dict, Any, Union
import openai
from dotenv import load_dotenv
import os


load_dotenv()


class LLMClient(ABC):
    """
    Abstrakte Schnittstelle für verschiedene LLMs.
    """

    @abstractmethod
    def analyze_prompt(self, system_msg: str, user_msg: str) -> Dict[str, Any]:
        """
        Analysiere einen Benutzer-Prompt und gebe eine strukturierte Antwort zurück.
        Args:
            system_msg (str): Systemnachricht (z. B. Kontext oder Anweisungen für das LLM).
            user_msg (str): Benutzer-Prompt.

        Returns:
            Dict[str, Any]: Antwort des LLMs.
        """
        pass

# Factory-Funktion zur Auswahl des LLM-Clients
def create_llm_client(client_type: str) -> LLMClient:
    if client_type == "openai":
        return OpenAIClient()
    elif client_type == "huggingface":
        return HuggingFaceClient()
    else:
        raise ValueError(f"Unbekannter LLM-Client-Typ: {client_type}")

class OpenAIClient(LLMClient):
    """
    OpenAI-Implementierung der LLM-Schnittstelle.
    """

    def __init__(self):
        """
        Initialisiert den OpenAI-Client mit einem API-Schlüssel aus Umgebungsvariablen.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY nicht in den Umgebungsvariablen gefunden.")
        openai.api_key = self.api_key


    def analyze_prompt(self, system_msg: str, user_msg: str) -> Union[str, Any]:
        """
        Analysiere einen Prompt und gebe eine Antwort zurück.
        Args:
            system_msg (str): Systemnachricht (z. B. Anweisungen oder Kontext).
            user_msg (str): Benutzer-Prompt.

        Returns:
            Dict[str, Any]: Antwort des LLMs.
        """
        try:
            # Anfrage an OpenAI
            response = openai.Client().chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=200,
                temperature=0.7,
            )
            # Antwort extrahieren
            return response.choices[0].message.content
        except Exception as e:
            print(f"Fehler bei der Anfrage: {e}")
            return f"Fehler: {e}"


class HuggingFaceClient(LLMClient):
    """
    Hugging Face-Implementierung der LLM-Schnittstelle.
    """
    def __init__(self):
        """
        Initialisiert den Hugging Face-Client mit einem API-Schlüssel aus Umgebungsvariablen.
        """
        self.api_key = os.getenv("KARLI_API_KEY")
        if not self.api_key:
            raise ValueError("KARLI_API_KEY nicht in den Umgebungsvariablen gefunden.")
        self.api_url = os.getenv("API_URL")
        if not self.api_url:
            raise ValueError("KARLI_API_KEY nicht in den Umgebungsvariablen gefunden.")

    def analyze_prompt(self, system_msg: str, user_msg: str) -> Dict[str, Any]:
        import requests

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": f"{system_msg}\n\n{user_msg}",
            "parameters": {"max_length": 100},
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei der Anfrage an Hugging Face: {e}")
            return {"error": str(e)}
