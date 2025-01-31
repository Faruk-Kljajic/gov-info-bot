from abc import ABC, abstractmethod
from typing import Dict, Any, Union
from langchain_community.vectorstores import FAISS
from openai import OpenAI
from dotenv import load_dotenv
import os

from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from info_bot_backend.application.services.process_data import rag_process

from info_bot_backend.application.utils.constants import SYSTEM_MSG_2, SYSTEM_MSG_1

load_dotenv()


class LLMClient(ABC):
    """
    Abstrakte Schnittstelle für verschiedene LLMs.
    """

    @abstractmethod
    def analyze_prompt(self, user_msg: str) -> Dict[str, Any]:
        """
        Analysiere einen Benutzer-Prompt und gebe eine strukturierte Antwort zurück.
        Args:
            user_msg (str): Benutzer-Prompt.

        Returns:
            Dict[str, Any]: Antwort des LLMs.
        """
        pass

    @abstractmethod
    def create_response(self, user_msg):
        pass

    @abstractmethod
    def create_rag_prompt(self, system_msg: str, user_msg: str, data: str):
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

        # OpenAI-Client initialisieren
        self.client = OpenAI(api_key=self.api_key)

        # Initialisiere Embedding-Modell
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

        # Vectorstore-Speicherort definieren
        self.vectorstore_path = os.path.join("application/resources/faiss_index")

        # Vectorstore laden, falls vorhanden
        if os.path.exists(self.vectorstore_path):
            self.vectorstore = FAISS.load_local(self.vectorstore_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            self.vectorstore = None
            print(f"Kein Vectorstore gefunden unter {self.vectorstore_path}. Bitte sicherstellen, dass er existiert.")

        # Standardparameter für LLM
        self.default_model = "gpt-4"
        self.default_max_tokens = 300
        self.default_temperature = 0.7

    def create_response(self, user_msg):
        """
        Abstrahiert den LLM-Aufruf mit Standardparametern.

            Args:
                user_msg (str): Benutzer-Prompt.

            Returns:
                str: Generierte Antwort des LLM.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": SYSTEM_MSG_1},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=self.default_max_tokens,
                temperature=self.default_temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Fehler bei der Anfrage: {e}")
            return f"Fehler: {e}"

    def analyze_prompt(self, user_msg: str) -> Union[str, Any]:
        """
        Analysiert einen Prompt und gibt eine Antwort zurück.
            - Prüft, ob ein Vectorstore vorhanden ist.
            - Falls kein Vectorstore vorhanden ist, wird `rag_process` aufgerufen, um einen zu erstellen.
            - Gibt eine Fehlermeldung zurück, wenn ein Problem beim Abrufen der Daten besteht.
            - Nutzt LLM, um basierend auf dem Vectorstore und dem Prompt die Frage zu beantworten.

        Args:
            user_msg (str): Benutzer-Prompt.

        Returns:
            str: Generierte Antwort oder Fehlermeldung.
        """
        try:
            # 1. Prüfen, ob Vectorstore vorhanden ist
            if not self.vectorstore:
                print("Kein Vectorstore gefunden. Starte den RAG-Prozess...")
                result = rag_process()  # Rufe die Methode für den RAG-Prozess auf
                print(result)
                # 2. Nach dem RAG-Prozess erneut prüfen
                if "Fehler" in result:
                    print("Vectorstore konnte nicht erstellt werden.")
                    return "Fehler: Es gibt aktuell Probleme mit dem Datenabruf. Bitte versuchen Sie es später erneut."

             # Vectorstore laden, falls vorhanden
            if os.path.exists(self.vectorstore_path):
                self.vectorstore = FAISS.load_local(self.vectorstore_path, self.embeddings, allow_dangerous_deserialization=True)
            # 3. Relevante Daten aus dem Vectorstore abrufen
            docs = self.vectorstore.similarity_search(user_msg, k=3)
            context = "\n".join([doc.page_content for doc in docs])

            # 4. LLM-Aufruf mit Kontext und Prompt
            prompt = (
                f"Hier sind die relevanten Informationen:\n{context}\n\n"
                f"Basierend auf diesen Informationen, beantworte bitte die folgende Frage:\n{user_msg}"
            )
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": SYSTEM_MSG_2},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
                temperature=0.7,
            )

            # 5. Antwort extrahieren und zurückgeben
            return response.choices[0].message.content

        except Exception as e:
            print(f"Fehler bei der Anfrage: {e}")
            return f"Fehler: {e}"

    def create_rag_prompt(self, system_msg: str, user_msg: str, data: str) -> str:
        """
        Erstellt eine Antwort basierend auf relevanten Daten, die explizit übergeben werden.

        Args:
            system_msg (str): Systemnachricht.
            user_msg (str): Benutzer-Prompt.
            data (str): Relevante Daten für die Antwort.

        Returns:
            str: Generierte Antwort des LLM.
        """
        try:
            # Prompt für das LLM erstellen
            prompt = PromptTemplate(
                input_variables=["data", "user_msg"],
                template=(
                    "Hier sind die relevanten Informationen:\n{data}\n\n"
                    "Basierend auf diesen Informationen, beantworte bitte die folgende Frage:\n{user_msg}"
                ),
            )
            # Anfrage an OpenAI senden
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt.format(data=data, user_msg=user_msg)},
                ],
                max_tokens=self.default_max_tokens,
                temperature=self.default_temperature,
            )

            # Antwort extrahieren
            return response.choices[0].message.content
        except Exception as e:
            print(f"Fehler bei der Anfrage: {e}")
            return f"Fehler: {e}"

#HuggingFace wurde nur zum Testen verwendet

#HuggingFace wurde nur zum Testen verwendet
class HuggingFaceClient(LLMClient):
    """
    Hugging Face-Implementierung der LLM-Schnittstelle.
    """

    def create_rag_prompt(self, system_msg: str, user_msg: str, data: str):
        pass

    def create_response(self, user_msg):
        pass

    def __init__(self):
        """
        Initialisiert den Hugging Face-Client mit einem API-Schlüssel aus Umgebungsvariablen.
        """
        pass

    def analyze_prompt(self, user_msg: str) -> Dict[str, Any]:
        pass
