import json
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from info_bot_backend.application.services.data_search import DataService
from info_bot_backend.application.utils.constants import FILE_NAME_JSON, SEARCH_KEY, JSON_FILE_URL


#  JSON-Datei laden
def load_json_file(file_name):
    """
    Versucht, die JSON-Datei aus dem Ordner resources zu laden.
    Falls sie nicht existiert, wird eine Datensuche durchgeführt.

    Args:
        file_name (str): Der Name der Datei (z. B. 'wahl_20241003_214746.json').

    Returns:
        dict: Geladene JSON-Daten.
    """
    # Absoluter Pfad zum resources-Ordner
    resources_path = os.path.join("../resources/downloads", file_name)

    try:
        # Prüfen, ob die Datei existiert
        if os.path.exists(resources_path):
            # Datei laden
            with open(resources_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            print(f"Datei erfolgreich geladen: {resources_path}")
            return data
        else:
            # Wenn die Datei nicht existiert, starte Datensuche
            print(f"Datei nicht gefunden: {resources_path}. Starte Datensuche...")
            service = DataService()
            service.download_json(JSON_FILE_URL, FILE_NAME_JSON)
            return load_json_file(FILE_NAME_JSON)
    except Exception as e:
        print(f"Fehler beim Laden der Datei: {e}")
        raise

# Daten verarbeiten
def process_data(json_data):
    documents = []
    for key, values in json_data.items():
        gebietsname = values.get("gebietsname", "Unbekannt")
        wahlberechtigt = values.get("wahlberechtigt", "0")
        abgegeben = values.get("abgegeben", "0")
        ungueltig = values.get("ungueltig", "0")
        gueltig = values.get("gueltig", "0")

        # Erstelle einen lesbaren Text für Parteien und ihre Stimmen
        ergebnisse = "\n".join([f"{partei}: {stimmen}"
                                for partei, stimmen in values.items()
                                if
                                partei not in {"gebietsname", "wahlberechtigt", "abgegeben", "ungueltig", "gueltig"}])

        # Formatierter Text pro Gebiet
        text = (
            f"Gebietsname: {gebietsname}\n"
            f"Wahlberechtigte: {wahlberechtigt}\n"
            f"Abgegebene Stimmen: {abgegeben}\n"
            f"Ungültige Stimmen: {ungueltig}\n"
            f"Gültige Stimmen: {gueltig}\n"
            f"Ergebnisse:\n{ergebnisse}"
        )
        documents.append(text)
    return documents


# Text in Abschnitte unterteilen
def split_documents(documents, chunk_size=1000, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    splitted_docs = text_splitter.create_documents(documents)
    return splitted_docs


# Embeddings erstellen
def generate_embeddings(documents, embedding_model="text-embedding-ada-002"):
    embeddings = OpenAIEmbeddings(model=embedding_model)
    return embeddings


# FAISS-Index erstellen
def create_faiss_index(documents, embeddings):
    vectorstore = FAISS.from_texts([doc.page_content for doc in documents], embeddings)
    return vectorstore


# Index speichern
def save_faiss_index(vectorstore, file_path):
    vectorstore.save_local(file_path)

def rag_process(chunk_size=1000, chunk_overlap=50, embedding_model="text-embedding-ada-002") -> str:
    """
    Hauptprozess, der die Daten verarbeitet, in Abschnitte unterteilt,
    Embeddings erstellt und den FAISS-Index speichert.

    Args:
        chunk_size (int): Die Größe der Textabschnitte.
        chunk_overlap (int): Die Überlappung zwischen den Abschnitten.
        embedding_model (str): Das Modell für die Embeddings.
    """
    try:
        # 1. JSON-Datei laden
        json_data = load_json_file(FILE_NAME_JSON)

        # 2. Daten verarbeiten
        documents = process_data(json_data)

        # 3. Dokumente in Abschnitte unterteilen
        splitted_docs = split_documents(documents, chunk_size, chunk_overlap)

        # 4. Embeddings erstellen
        embeddings = generate_embeddings(splitted_docs, embedding_model)

        # 5. FAISS-Index erstellen
        vectorstore = create_faiss_index(splitted_docs, embeddings)

        # 6. FAISS-Index speichern
        index_path = os.path.join("../resources/faiss_index")
        save_faiss_index(vectorstore, index_path)

        return f"RAG-Prozess erfolgreich abgeschlossen. FAISS-Index gespeichert unter: {index_path}"
    except Exception as e:
        return f"Fehler im RAG-Prozess: {e}"