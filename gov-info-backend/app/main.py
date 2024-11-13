from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from .routes.botAPI import frage_chatbot

app = FastAPI()

# Hinzufügen der CORS-Middleware direkt nach der App-Instanz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Stelle sicher, dass das die exakte URL des Frontends ist
    allow_credentials=True,
    allow_methods=["*"],  # Alle Methoden erlauben
    allow_headers=["*"],  # Alle Header erlauben
)

class Message(BaseModel):
    message: str

@app.get("/")
async def read_root():
    return {"message": "Hello, Chatbot Backend is running!"}

@app.post("/chat/")
async def chat_response(message: Message):
    try:
        response = frage_chatbot(message.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
