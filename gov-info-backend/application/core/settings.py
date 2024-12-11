# core/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Automatisches Finden des Projekt-Root-Verzeichnisses
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Passe an, falls die Struktur anders ist

# Lade die .env-Datei aus dem Root-Verzeichnis
dotenv_path = BASE_DIR / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(f".env-Datei nicht gefunden: {dotenv_path}")

class Settings(BaseSettings):
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./test.db"
    OPENAI_API_KEY: str  # Pflichtfeld

    class Config:
        env_file = str(dotenv_path)  # Redundante Sicherheit

settings = Settings()

