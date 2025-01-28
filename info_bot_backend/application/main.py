from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from info_bot_backend.application.api_endpoint import chat
from info_bot_backend.application.utils.constants import CONFIG_CONSTANT

app = FastAPI(
    title="Chatbot Backend",
    description="Backend für den Advanced RAG Chatbot",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, tags=["Chat"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": f"Willkommen! Aktive Konfiguration: {CONFIG_CONSTANT}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

