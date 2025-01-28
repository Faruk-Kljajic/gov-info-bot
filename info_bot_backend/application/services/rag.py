from langchain.vectorstores import FAISS

# FAISS-Index laden
def load_faiss_index(file_path, embeddings):
    """
    Lädt einen FAISS-Index aus einem lokalen Speicherort.

    Args:
        file_path (str): Pfad zum gespeicherten FAISS-Index.
        embeddings: Embedding-Modell, das beim Laden benötigt wird.

    Returns:
        FAISS: Geladener FAISS-Index.
    """
    return FAISS.load_local(file_path, embeddings)


# Abfrage durchführen
def query_faiss_index(vectorstore, query, k=3):
    """
    Führt eine Ähnlichkeitssuche im FAISS-Index durch.

    Args:
        vectorstore (FAISS): Geladener FAISS-Index.
        query (str): Die Benutzerabfrage.
        k (int): Anzahl der zurückzugebenden Ergebnisse.

    Returns:
        list: Eine Liste ähnlicher Dokumente.
    """
    docs = vectorstore.similarity_search(query, k=k)
    return docs