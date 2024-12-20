from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from application.api.endpoints import chat, upload
from application.core.settings import settings
from application.core.config import CONFIG_CONSTANT


app = FastAPI(
    title="Chatbot Backend",
    description="Backend für den Advanced RAG Chatbot",
    version=settings.APP_VERSION  # Zugriff auf die Version aus settings
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
#app.include_router(upload.router, prefix="/upload", tags=["Upload"])


@app.get("/", tags=["Root"])
async def root():
    return {"message": f"Willkommen! Aktive Konfiguration: {CONFIG_CONSTANT}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

