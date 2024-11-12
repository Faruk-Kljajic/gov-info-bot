from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .routes.botAPI import frage_chatbot  # Importiere die Chatbot-Funktion

app = FastAPI()

# Anfrage-Datenstruktur
class Message(BaseModel):
    message: str

@app.get("/")
async def read_root():
    return {"message": "Hello, Chatbot Backend is running!"}

@app.post("/chat/")
async def chat_response(message: Message):
    try:
        # Chatbot-Logik aufrufen
        response = frage_chatbot(message.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
