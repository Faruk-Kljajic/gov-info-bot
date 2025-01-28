import requests
import os

from info_bot_backend.application.utils.constants import DATA_GOV_AT_URL


class DataService:
    BASE_URL = DATA_GOV_AT_URL

    def __init__(self, download_folder="../resources/downloads"):
        """
        Initialisiert den DataService.
        :param download_folder: Ordner, in dem Dateien gespeichert werden.
        """
        self.download_folder = download_folder
        os.makedirs(download_folder, exist_ok=True)

    def autocomplete_packages(self, query, limit=3):
        """
        Sucht Datensätze (Packages) basierend auf einem Suchbegriff.
        :param query: Suchbegriff für die Paketnamen oder Titel.
        :param limit: Maximale Anzahl der zurückgegebenen Ergebnisse.
        :return: Liste der gefundenen Datensätze (Name und Titel).
        """
        url = f"{self.BASE_URL}/package_autocomplete"
        params = {"q": query, "limit": limit}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                print(f"API-Ergebnisse: {data['result']}")  # Debugging
                # Rückgabe von `name` und `title`
                return [{"name": pkg["name"], "title": pkg["title"]} for pkg in data["result"]]
            else:
                print(f"API-Fehler: {data.get('error')}")
                return []
        except requests.RequestException as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return []

    def get_package_details(self, package_id):
        """
        Ruft die Details eines Pakets ab.
        :param package_id: ID des Pakets.
        :return: Paketdetails als Dictionary.
        """
        url = f"{self.BASE_URL}/package_show"
        params = {"id": package_id}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                return data["result"]
            else:
                print(f"API-Fehler: {data.get('error')}")
                return None
        except requests.RequestException as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None

    def download_csv(self, resource_url, filename):
        """
        Lädt eine Datei herunter und speichert sie lokal.
        :param resource_url: URL der Ressource.
        :param filename: Name der gespeicherten Datei.
        :return: Lokaler Pfad zur gespeicherten Datei.
        """
        local_path = os.path.join(self.download_folder, filename)

        try:
            response = requests.get(resource_url)
            response.raise_for_status()

            with open(local_path, "wb") as file:
                file.write(response.content)

            print(f"Datei gespeichert unter: {local_path}")
            return local_path
        except requests.RequestException as e:
            print(f"Fehler beim Herunterladen der Datei: {e}")
            return None

    def fetch_and_download_data(self, query):
        """
        Führt die gesamte Logik aus: Suche, Details abrufen und Download.
        :param query: Suchbegriff für die Datensätze.
        """
        # Schritt 1: Suche nach Datensätzen
        datasets = self.autocomplete_packages(query, limit=5)
        if not datasets:
            print("Keine Datensätze gefunden.")
            return

        print("Gefundene Datensätze:")
        for dataset in datasets:
            print(f"- {dataset['title']} (Name: {dataset['name']})")

        # Schritt 2: Für jeden Datensatz die Ressourcen abrufen und herunterladen
        for dataset in datasets:
            details = self.get_package_details(dataset["name"])
            if not details:
                continue

            print(f"\nRessourcen für Datensatz: {details['title']}")
            for resource in details.get("resources", []):
                # Beschränkung auf JSON und CSV
                if resource["format"].lower() in ["csv", "json"]:
                    print(f"- Ressource: {resource['name']} ({resource['format']})")
                    print(f"  URL: {resource['url']}")

                    # Herunterladen der Datei
                    filename = resource["name"].replace(" ", "_")
                    if not filename.endswith(f".{resource['format'].lower()}"):
                        filename += f".{resource['format'].lower()}"
                    self.download_csv(resource["url"], filename)
                else:
                    print(f"Übersprungene Ressource (nicht JSON/CSV): {resource['name']} ({resource['format']})")