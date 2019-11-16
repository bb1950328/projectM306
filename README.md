# Projekt M306 (Zeiterfassung)

## How to Projekt einrichten

Zur Vorbereitung mysql Server installieren. Als Passwort für root zur Einfachheit halber "root" wählen.

### Mit PyCharm

1. Mit VCS -> Check out from version control -> Git
 <https://github.com/bb1950328/projectM306.git>
2. venv.zip in Unterordner venv/ entpacken
3. Run configuration "manage.py migrate" starten
2. Run configuration "setup_database() && insert_test_data()" starten
4. Run configuration "project M306" starten

### Ohne PyCharm

1. Mit Git auschecken: <https://github.com/bb1950328/projectM306.git>
2. venv.zip in Unterordner venv/ entpacken
3. Terminal öffnen in Projekt Ordner
4. Folgende Befehle ausführen: 
   `.\venv\bin\actibate.bat`
   
   `python manage.py runserver 8000`
   
   `python .\time_entry\model\db.py setup_database insert_test_data`
   
   `python manage.py runserver 8000`
   
## Datenbank-Konfiguration anpassen

Die Datei `database_settings.json.default` nach `database_settings.json` kopieren. Eventuell Verbindungsparameter in der Datei anpassen.

## Ausprobieren

Die Seite ist unter <http://127.0.0.1:8000/> abrufbar.
