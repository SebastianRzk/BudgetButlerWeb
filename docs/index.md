# BudgetButlerWeb

* TOC
{:toc}

## Idee

* Einfache lokale Datenhaltung: Die Daten sind im CSV-Format gespeichert und damit mit einem Textverarbeitungsprogramm oder einem Tabellenverarbeitungsprogramm zugänglich.
* Unkomplizierte Einnahmen/Ausgaben-Rechnung, keine doppelte Buchführung.
* Schlanke Begleiter-Web-App für unterwegs (online-Version, mobil-optimiert). Automatisierter Import der Daten in die lokale Anwendung
* Schlankes und minimalistisches Design
* Hohe Geschwindigkeit, auch bei großen Datenmengen
* Quelloffen
* Individualisierbar

## Merkmale

* Einzelbuchungen
  * Einzelbuchungen (erfassen, ändern, löschen)
  * Daueraufträge (erfassen, ändern (auch nachträglich), Betrag innerhalb der Ausführung anpassen, löschen)
  * Monatsübersicht
  * Jahresübersicht
  * Automatischer Import von Sparbuchungen, Order sowie gemeinsamen Buchungen in die "Einzelbuchungen"-Gesamtübersicht
  * Import von Einzelbuchungen aus der Begleiter Web-App


* Gemeinsame Buchungen
  * Erfassen, Ändern, Löschen
  * Abrechnung erstellen
  * Abrechnungen exportieren und importieren
  * Import von gemeinsame Buchungen aus der Begleiter Web-App


* Sparen
  * Erfassen, Ändern und Löschen von Sparkontos, Sparbuchungen, Depots, Depotwerte (mit Typ: ETF, Fond, Einzelaktie, Crypto oder Robo), Order, Order-Daueraufträgen sowie Depotauszüge
  * Sparen Übersicht:
    * Vergleich: Einnahmen, Ausgaben und Sparen über die Zeit
    * Zusammensetzung der Sparanlage
  * ETF-Portfolio Vergleichen: Kosten, Sektoren und Länder jeweils pro ETF und nach Anteil im Portfolio


* Konfiguration
  * Farbthema anpassen
  * Farben der Kategorien anpassen
  * Verwendung mehrerer Datenbanken
  * Backup der Datenbank-Datei anlegen
  * Kategorien übergreifend umbenennen
  * Kategorien für Eingabefelder ausschließen

## Weiterführende Links

* Fehler, Fragen, Anmerkungen oder Ideen gerne als ["ISSUE" hier hinterlassen](https://github.com/SebastianRzk/BudgetButlerWeb/issues)
* Code-Änderungen (Pull-Requests) immer bitte immer gegen den `dev`-[Branch hier hin](https://github.com/SebastianRzk/BudgetButlerWeb/pulls)
* [Hier liegt der blanke Code](https://github.com/SebastianRzk/BudgetButlerWeb)
* [Hier liegen die Docker-Images für die Begleiter Web-App](https://hub.docker.com/u/sebastianrzk), und [hier sind Deployment Beispiele für die Begleiter Web-App](https://github.com/SebastianRzk/BudgetButlerWeb/tree/master/butler_online_distribution)


## Screenshots

### Screenshots BudgetButlerWeb Offline Anwendung

<img src="img/screenshots_desktop/dashboard.png" alt="Dashboard" width="300"/>

#### Einzelbuchungen

<a href="img/screenshots_desktop/einzelbuchungen_add.png"><img src="img/screenshots_desktop/einzelbuchungen_add.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_desktop/uebersicht_einzelbuchungen.png"><img src="img/screenshots_desktop/uebersicht_einzelbuchungen.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_desktop/dauerauftraege_add.png"><img src="img/screenshots_desktop/dauerauftraege_add.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_desktop/uebersicht_dauerauftraege.png"><img src="img/screenshots_desktop/uebersicht_dauerauftraege.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_desktop/uebersicht_jahr.png"><img src="img/screenshots_desktop/uebersicht_jahr.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_desktop/uebersicht_monat.png"><img src="img/screenshots_desktop/uebersicht_monat.png" alt="Dasboard" width="300"/></a>

#### Gemeinsame Buchungen
<a href="img/screenshots_desktop/add_gemeinsam.png"><img src="img/screenshots_desktop/add_gemeinsam.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_desktop/gemeinsam_abrechnen.png"><img src="img/screenshots_desktop/gemeinsam_abrechnen.png" alt="Dasboard" width="300"/></a>

#### Sparen

<a href="img/screenshots_desktop/sparen_uebersicht.png"><img src="img/screenshots_desktop/sparen_uebersicht.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_desktop/sparen_uebersicht_depotwerte.png"><img src="img/screenshots_desktop/sparen_uebersicht_depotwerte.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_desktop/sparen_uebersicht_etfs.png"><img src="img/screenshots_desktop/sparen_uebersicht_etfs.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_desktop/sparen_uebersicht_sparkontos.png"><img src="img/screenshots_desktop/sparen_uebersicht_sparkontos.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_desktop/sparen_add_depotauszug.png"><img src="img/screenshots_desktop/sparen_add_depotauszug.png" alt="Dasboard" width="300"/></a>


### Screenshots Begleiter Web-App

<a href="img/screenshots_mobile/menu.png"><img src="img/screenshots_mobile/menu.png" alt="Dasboard" width="250"/></a>
<a href="img/screenshots_mobile/erfassen.png"><img src="img/screenshots_mobile/erfassen.png" alt="Dasboard" width="250"/></a>
<a href="img/screenshots_mobile/erfassen_desktop.png"><img src="img/screenshots_mobile/erfassen_desktop.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_mobile/gemeinsam.png"><img src="img/screenshots_mobile/gemeinsam.png" alt="Dasboard" width="250"/></a>
<a href="img/screenshots_mobile/einzel.png"><img src="img/screenshots_mobile/einzel.png" alt="Dasboard" width="250"/></a>
<a href="img/screenshots_mobile/einzel.png"><img src="img/screenshots_mobile/erfassen_dauerauftrag.png" alt="Dasboard" width="250"/></a>
<a href="img/screenshots_mobile/einzel.png"><img src="img/screenshots_mobile/uebersicht_dauerauftrag.png" alt="Dasboard" width="250"/></a>


## Offline Anwendung: BudgetButlerWeb

### Systemvoraussetzungen

* Python 3.10+
* Pip
* Versionierung: git
* Anwendungsicon sowie Startup-Skript: shell und npm (für Electron-Client)
* Falls nicht der Electron-Client verwendet wird: Webbrowser (z.B. Firefox oder Chromium)

### Installation

Das Git-Repository klonen:

	git clone https://github.com/SebastianRzk/BudgetButlerWeb.git

Ins Projektverzeichnis wechseln:

	cd BudgetButlerWeb

Optional: Anwendungsicon anlegen:

    sh create_shortcut.sh

### BudgetButlerWeb starten

Die Applikation kann über das Anwendungsicon gestartet werden. Der erste Start dauert durch die Installation der benötigten Abhängigkeiten etwas länger. Dies ist nur beim ersten Start der Anwendung nach dem Klonen des Repositories notwendig.


Alternativ kann das Start-Skript manuell aufgerufen werden. Dieses startet das Backend und das Frontend automatisch. Beim ersten Start werden ggf. fehlende Abhängigkeiten nachinstalliert (für Python über `venv` und `pip`, `npm` installiert den Electron-Client):

	sh start_butler_offline.sh


Alternativ kann der Server auch manuell gestartet werden:

    # venv anlegen
    python -m venv venv
    # venv aktivieren
    source venv/bin/activate
    # Abhängigkeiten installieren (falls nicht schon passiert)
    pip install -r butler_offline/requirements.txt
    # Flask starten
    flask --app butler_offline run

Über ein Webbrowser kann die Webseite nun lokal erreicht werden:

    http://localhost:5000
    


### Softwaretests ausführen

Alle Softwaretests mit pytest starten:

	pytest butler_offline

Testabdeckung mit pytest berechnen:

	pytest butler_offline --cov

### Updates

BudgetButlerWeb aktualisieren:

	git pull
    # Abhängigkeiten aktualisieren
    rm -rfv venv
    rm -rfv butler_offline_client/node_modules



## Umgebungsvariablen


| Wert                                 | Default     | Beschreibung                                            |
|--------------------------------------|-------------|---------------------------------------------------------|
| BUDGETBUTLERWEB_DATABASE_PATH        | ..          | Ordner an dem die Datenbanken gesucht werden sollen.    |
| BUDGETBUTLERWEB_CONFIG_PATH          | ..          | Ordner an dem die Configuration gesucht werden soll.    |
| BUDGETBUTLERWEB_DATABASE_BACKUP_PATH | ../Backups  | Ordner in welchem die Datenbank-Backups abgelegt werden |


## Begleiter Web-App:

### Build

#### Anforderungen zum Build

##### Build in der Entwicklungsumgebung

Systemanforderungen: 

* npm
* rust und mysql library (z.B. MariaDB)

Vorgehen:

* Frontend:

  * In das Verzeichnis `butler_online/budgetbutler` wechseln
  * Mit `npm install` fehlende Abhängigkeiten installieren
  * Angular-Build anstoßen `npm run build -- --configuration=production`

* Backend:

  * In das Verzeichnis `butler_online_api` wechseln
  * Rust-Build anstoßen `cargo build --release`

oder:

Systemanforderungen:

* docker (und docker-compose)

Vorgehen:

* In das Verzeichnis `butler_online_distribution/budget_butler_local_build` wechseln
* Build-Skript ausführen: `sh build_and_run_it.sh`



###  Betrieb:

Systemanforderungen für den Betrieb:

* docker und docker-compose

Ein Beispiel-Docker-Compose-File kann in `butler_online_distribution/budget_butler` eingesehen werden.
Für den Betrieb müssen in `api.env` sowie in `db.env` Parameter beispielsweise für den OAuth-Flow ergänzt werden.


## Ideen für die Zukunft / bekannte Limitierungen

### BudgetButlerWeb Offline

* Aktuell werden die Daten nur für eine retrospektive Visualisierung verwendet. Dabei könnte man die Daten auch für eine Projektion in die Zukunft verwenden. Dies konnte bei den Einnahmen/ Ausgaben sowie auch bei den Spar-Plänen nützlich sein.
* Implementierung von Tags an Einzelbuchung, um neben den der "Kategorie" noch weitere sortier- und durchsuchbare Marker zur Verfügung zu stellen. (Zum Beispiel Marker wie "steuerlich absetzbar" oder "Weihnachtsgeschenke" oder "Sommerurlaub")
* BudgetButlerWeb Anwendung im AUR verfügbar machen, damit Aktualisierungen automatisch über yay durchgeführt werden.
* Codequalität und Testabdeckung automatisiert und langfristig tracken (z.B. durch SonarCloud)

### BudgetButlerWeb Begleiter App

* Codequalität und Testabdeckung automatisiert und langfristig tracken (z.B. durch SonarCloud)

