from typing import Any

from application.services.llm_client import LLMClient


class LLMService:
    """
    Service, um mit verschiedenen LLMs zu interagieren.
    """

    def __init__(self, llm_client: LLMClient):
        """
        Initialisiert den Service mit einem spezifischen LLM-Client.
        Args:
            llm_client (LLMClient): Instanz eines LLM-Clients.
        """
        self.llm_client = llm_client

    def analyze_prompt(self, user_msg: str) -> dict[str, Any]:
        """
        Übermittle den Prompt an das LLM und erhalte eine Antwort.
        Args:
            user_msg (str): Benutzer-Prompt.

        Returns:
            str: Antwort des LLMs als Text.
        """
        print(user_msg)
        # Hier könnte ein Aufruf des LLM-Clients erfolgen
        return self.llm_client.analyze_prompt(
            system_msg="Du bist ein hilfreicher Assistent.",
            user_msg=user_msg,
        )

