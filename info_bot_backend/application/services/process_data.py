import json
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from info_bot_backend.application.services.data_search import DataService
from info_bot_backend.application.utils.constants import FILE_NAME_JSON


# 1. JSON-Datei laden
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
    resources_path = os.path.join(os.path.dirname(__file__), "../resources/downloads", file_name)

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
            service.fetch_and_download_data("Nationalratswahl 2024")
            return load_json_file(FILE_NAME_JSON)
    except Exception as e:
        print(f"Fehler beim Laden der Datei: {e}")
        raise

# 2. Daten verarbeiten
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


# 3. Text in Abschnitte unterteilen
def split_documents(documents, chunk_size=1000, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    splitted_docs = text_splitter.create_documents(documents)
    return splitted_docs


# 4. Embeddings erstellen
def generate_embeddings(documents, embedding_model="text-embedding-ada-002"):
    embeddings = OpenAIEmbeddings(model=embedding_model)
    return embeddings


# 5. FAISS-Index erstellen
def create_faiss_index(documents, embeddings):
    vectorstore = FAISS.from_texts([doc.page_content for doc in documents], embeddings)
    return vectorstore


# 6. Index speichern
def save_faiss_index(vectorstore, file_path):
    vectorstore.save_local(file_path)


# 7. FAISS-Index laden
def load_faiss_index(file_path, embeddings):
    return FAISS.load_local(file_path, embeddings)


# 8. Abfrage durchführen
def query_faiss_index(vectorstore, query, k=3):
    docs = vectorstore.similarity_search(query, k=k)
    return docs