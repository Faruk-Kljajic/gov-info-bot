from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from application.services.rag import process_query
from application.api.dependencies import get_csv_data, get_llm_instance

router = APIRouter()

# Anfrage-Modell
class ChatRequest(BaseModel):
    message: str


# Chat-Endpunkt
@router.post("/api/chat")
async def chatbot_endpoint(
    request: ChatRequest,
    csv_data=Depends(get_csv_data),
    llm_instance=Depends(get_llm_instance),
):
    """
    Haupt-Endpunkt für den Chatbot:
    - Verarbeitet eine Benutzerfrage.
    - Nutzt RAG-Service für die Antwortgenerierung.
    """
    try:
        # Process the user question through the RAG pipeline
        response = process_query(csv_data, llm_instance, request.message, None,
                                 None)  # Region and party extraction handled in the service
        return {"question": request.message, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
