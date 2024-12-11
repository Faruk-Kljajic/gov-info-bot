import pandas as pd
from typing import Optional

def filter_data(
    df: pd.DataFrame,
    gebiet: Optional[str] = None,
    partei: Optional[str] = None,
    weitere_kriterien: Optional[dict] = None,
    sortiere_nach: Optional[str] = None,
    min_abgegebene: Optional[int] = None,
) -> str:
    """
    Filtert die CSV-Daten basierend auf Gebiet, Partei und zusätzlichen Kriterien.

    :param df: Der DataFrame mit den Wahldaten.
    :param gebiet: Das zu filternde Gebiet.
    :param partei: Die zu filternde Partei.
    :param weitere_kriterien: Zusätzliche Filterkriterien als Dictionary.
    :param sortiere_nach: Spalte, nach der die Ergebnisse sortiert werden sollen.
    :param min_abgegebene: Mindestanzahl an abgegebenen Stimmen.
    :return: Ein String mit den gefilterten Ergebnissen.
    """
    if df.empty:
        return "Die Wahldaten konnten nicht geladen werden."

    gefilterte_daten = df

    # Filter nach Gebiet
    if gebiet:
        gefilterte_daten = gefilterte_daten[
            gefilterte_daten["Gebietsname"].str.contains(gebiet, case=False, na=False)
        ]

    # Filter nach Partei
    if partei:
        if partei in gefilterte_daten.columns:
            gefilterte_daten = gefilterte_daten[["Gebietsname", partei]]
        else:
            return f"Die Partei '{partei}' wurde in den Daten nicht gefunden."

    # Zusätzliche Kriterien
    if weitere_kriterien:
        for spalte, wert in weitere_kriterien.items():
            if spalte in gefilterte_daten.columns:
                gefilterte_daten = gefilterte_daten[
                    gefilterte_daten[spalte].str.contains(str(wert), case=False, na=False)
                ]

    # Mindestanzahl an abgegebenen Stimmen
    if min_abgegebene:
        gefilterte_daten = gefilterte_daten[gefilterte_daten["Abgegebene"] >= min_abgegebene]

    # Sortiere nach Spalte
    if sortiere_nach and sortiere_nach in gefilterte_daten.columns:
        gefilterte_daten = gefilterte_daten.sort_values(by=sortiere_nach, ascending=False)

    # Überprüfung, ob nach dem Filtern noch Daten vorhanden sind
    if gefilterte_daten.empty:
        return "Keine passenden Daten gefunden."

    # Konvertiere die gefilterten Daten in einen String
    return gefilterte_daten.to_string(index=False)

