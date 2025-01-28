from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from info_bot_backend.application.services.llm_service import LLMService
from info_bot_backend.application.services.llm_client import create_llm_client
from info_bot_backend.application.utils.constants import SYSTEM_MSG_1


router = APIRouter()

# Anfrage-Modell
class ChatRequest(BaseModel):
    message: str
    use_rag: bool = False  # Standardmäßig kein RAG verwenden


# Chat-Endpunkt
@router.post("/api/chat")
async def chatbot_endpoint(request: ChatRequest):

    """
    Haupt-Endpunkt für den Chatbot:
    - Gibt die empfangenen Parameter aus.
    - Gibt eine Bestätigung zurück.
    """
    print("Backend erreicht")
    # LLM über die Factory erstellen
    llm_client = create_llm_client(client_type="openai")  # 'openai'
    try:

        if request.use_rag:
            # RAG-Logik
            print("RAG-Logik wird ausgeführt.")
            # Erzeuge eine Instanz des LLMService mit dem Client
            llm_service = LLMService(llm_client=llm_client)
            response = llm_service.analyze_prompt(user_msg=request.message)
        else:
            # Direkte LLM-Kommunikation
            print("Direkte LLM-Logik wird ausgeführt.")
            response = llm_client.create_response(
                system_msg=SYSTEM_MSG_1,
                user_msg=request.message
            )

        # Antwort erstellen
        return {
            "question": request.message,
            "response": response
        }
    except Exception as e:
        # Fehlerbehandlung
        print(f"Fehler im Chatbot-Endpunkt: {e}")
        raise HTTPException(status_code=500, detail=f"Fehler: {str(e)}")
