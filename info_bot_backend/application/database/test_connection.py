# test_connection.py
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError

# Setze den Datenbank-URL entsprechend deinen Verbindungsdetails
DATABASE_URL = "postgresql+psycopg2://sara_faruk:pr_dke_gr_8@localhost/gov_info"

# Erstelle die Engine
engine = create_engine(DATABASE_URL)

def test_connection():
    try:
        # Versuche, die Verbindung herzustellen
        with engine.connect() as connection:
            # Verbindung erfolgreich
            print("Verbindung zur Datenbank erfolgreich.")

            # Prüfe, ob die Tabellen 'chat' und 'content' existieren
            inspector = inspect(connection)
            tables = inspector.get_table_names()
            print("Vorhandene Tabellen:", tables)

            if 'chat' in tables and 'content' in tables:
                print("Tabellen 'chat' und 'content' gefunden.")
            else:
                print("Eine oder beide Tabellen ('chat', 'content') fehlen.")

    except OperationalError as e:
        print("Fehler bei der Verbindung zur Datenbank:", e)

# Teste die Verbindung
if __name__ == "__main__":
    test_connection()
