# Gov Info Bot

Gov Info Bot ist ein Chatbot, der dynamische Antworten auf Anfragen basierend auf Daten von [data.gv.at](https://data.gv.at) liefert. Der Chatbot verwendet ein Retrieval-Augmented Generation (RAG)-Modell, um aktuelle Datenquellen zu durchsuchen und benutzerfreundliche Antworten zu generieren.

## Funktionen

- Beantwortet Fragen zu Nationalratswahlergebnisse, indem es auf Daten von data.gv.at zugreift
- Nutzung von FastAPI für das Backend
- Angular-Frontend zur Benutzerinteraktion
- Docker-Container für einfache Bereitstellung

## Installation

### Voraussetzungen

- Python 3.9+
- Node.js (für das Frontend)
- Docker

### Backend installieren

1. Wechsle in das Backend-Verzeichnis:

    ```bash
    cd backend
    ```

2. Installiere die Abhängigkeiten:

    ```bash
    pip install -r requirements.txt
    ```

3. Starte den Server:

    ```bash
    uvicorn main:app --reload
    ```

### Frontend installieren

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 18.2.7.

1. Wechsle in das Frontend-Verzeichnis:

    ```bash
    cd frontend
    ```

2. Installiere die Abhängigkeiten:

    ```bash
    npm install
    ```

3. Starte den Angular-Server:

    ```bash
    ng serve
    ```

## Nutzung

Greife im Browser auf das Angular-Frontend zu:

Das Frontend kommuniziert mit dem Backend, das auf `http://localhost:8000` läuft.

## Beitrag leisten

Beiträge sind willkommen! Erstelle einen Pull Request oder öffne ein Issue, um eine Diskussion zu starten.

## Lizenz

Dieses Projekt steht noch unter kein Lizenz.
