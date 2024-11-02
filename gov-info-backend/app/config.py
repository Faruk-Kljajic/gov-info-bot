from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_USER: str = "sara_faruk"
    DATABASE_PASSWORD: str = "pr_dke_gr_8"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "gov-info"

    # Verbindung als vollständige URI
    @property
    def database_url(self):
        return (
            f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env"  # Die Umgebungsvariablen werden aus der .env-Datei geladen

# Eine Instanz der Settings-Klasse erstellen
settings = Settings()