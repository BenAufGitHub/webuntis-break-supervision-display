# GERMAN | DEUTSCH

    Projekt: Pausenaufsichten-Fuer-Webuntis
    Autor: Ben Mette
    E-Mail: bmette.api@gmail.com
    Version: 1.0.0
    Funktion: aufwandsfreier Zugang zu den Pausenaufsichten auf WebUntis


## Benötigte Module:
    pip install webuntis
    pip install pyperclip


## Info zu Speicherung von Daten:
    Benutzerdaten werden für das Login gespeichert, um dieses zu vereinfachen.
    Dabei werden aber ausschließlich Schul- und Servername gespeichert,
    für die manuelle Änderung dieser Daten nach erstem Ausführen die Datei
    '{benutzer}\\.webuntis-breaks\\config.ini' nach Wunsch ändern.
    Hinweis: Das hinzufügen von Benutzername und Passwort birgt Sicherheitsrisiken, 
    tuen Sie dies nach eigenem Risiko.


### Ausführung (Beispiel):
    1. Erstelle main.py im aktuellen Ordner
    2. importiere src.Launcher
    3. src.Launcher.launch()

    oder

    3. src.Launcher.launch(session={webuntis.Session Objekt})

### Umwandlung zu .exe:
    1. pip install pyinstaller
    Windows
    2. führe 'pyinstaller --onefile --windowed --add-data "resources\appIcon.png;." .\main.py' im Ordner aus
    IOS
    2. führe 'pyinstaller --onefile --windowed --add-data "resources\appIcon.png:." .\main.py' im Ordner aus



# ENGLISH | ENGLISCH

    Project: webuntis-break-supervisions
    Autor: Ben Mette
    E-Mail: bmette.api@gmail.com
    Version: 1.0.0
    Funktion: easy access to break supervisions in WebUntis


## Required Modules:
    pip install webuntis
    pip install pyperclip


## Information for saving data:
    To ease the use, userdata will be saved for the login.
    Only school- and servername will be saved, for manual configurations, change the file
    at '{username}\\.webuntis-breaks\\config.ini' as you desire.
    Hint: Adding username and password imposes security breaches, only do it at your own risk.


### Run example:
    1. Create main.py in current directory
    2. import src.Launcher
    3. src.Launcher.launch()

    or

    3. src.Launcher.launch(session={webuntis.Session object})

### Bundling to .exe:
    1. pip install pyinstaller
    Windows
    2. run 'pyinstaller --onefile --windowed --add-data "resources\appIcon.png;." .\main.py' in the directory
    IOS
    2. run 'pyinstaller --onefile --windowed --add-data "resources\appIcon.png:." .\main.py' in the directory
   
## LICENSE NOTICE
    License information is convered in 'LICENSE.txt'.
    Linceses of imported modules are covered in 'python-webuntis_LICENSE.txt' and 'pyperclip_LICENSE.txt'.




