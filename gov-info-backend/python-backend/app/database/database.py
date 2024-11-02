import psycopg2

try:
    # Verbindung herstellen
    connection = psycopg2.connect(
        user="sara_faruk",
        password="pr_dke_gr_8",
        host="localhost",
        port="5432",
        database="gov_info"
    )

    # Ein Cursor-Objekt erstellen, um SQL-Abfragen auszuführen
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    print(f"Erfolgreich verbunden zur Datenbank: {db_version}")

except (Exception, psycopg2.DatabaseError) as error:
    print(f"Fehler beim Verbinden zur Datenbank: {error}")
finally:
    # Verbindung schließen, wenn sie besteht
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()
        print("Datenbankverbindung geschlossen.")