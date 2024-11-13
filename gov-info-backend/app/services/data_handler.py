import os
import pandas as pd

# CSV-Datei wird in ein DataFrame geladen
csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ressources', 'wahldaten2024.csv')
df = pd.read_csv(csv_path, encoding='ISO-8859-15', sep=";", on_bad_lines='skip')

# Funktion, um Ergebnis
# se für ein bestimmtes Gebiet zu holen
def get_results_for_region(region):
    # Filtere das DataFrame nach dem angegebenen Gebiet
    region_data = df[df['Gebietsname'] == region]

    if region_data.empty:
        return f"Es wurden keine Ergebnisse für das Gebiet '{region}' gefunden."

    # Ergebnisse formatieren
    results = f"Wahlergebnisse: "
    for col in region_data.columns[1:]:  # die erste Spalte wird übersprungen, weil sich darin die Spaltenbezeichnung befindet
        results += f"{col}: {region_data.iloc[0][col]}\n"

    return results
