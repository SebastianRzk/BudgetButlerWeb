# Offline Anwendung: BudgetButlerWeb

## Menu

### Weitere Seiten

* [Hauptseite](index.md)
* [Companion-App](butler-companion)

### Inhaltsverzeichnis

* [Systemvoraussetzungen](#systemvoraussetzungen)
* [Installation](#installation)
* [BudgetButlerWeb starten](#budgetbutlerweb-starten)
* [Umgebungsvariablen](#umgebungsvariablen)
* [Migration von Version 3.0.0 auf 4.0.0 (von Python Client auf Rust Client)](#migration-von-version-300-auf-400-von-python-client-auf-rust-client)

## Systemvoraussetzungen

* Rust / Cargo
* Versionierung: git
* Anwendungsicon sowie Startup-Skript: shell und npm (für Electron-Client)
* Falls nicht der Electron-Client verwendet wird: Webbrowser (z.B. Firefox oder Chromium)

## Installation

Das Git-Repository klonen:

	git clone https://github.com/SebastianRzk/BudgetButlerWeb.git

Ins Projektverzeichnis wechseln:

	cd BudgetButlerWeb

Anwendung bauen

    sh build.sh

Optional: Anwendungsicon anlegen:

    sh create_desktop_shortcut.sh

## BudgetButlerWeb starten

Die Applikation kann über das Anwendungsicon gestartet werden

Alternativ kann der Electron Client manuell gestartet werden, dieser startet das Rust-Backend automatisch und stoppt
dieses, wenn das Fenster geschlossen wird.

	cd ./target/ && ./application-wrapper/budgetbutlerweb

Alternativ kann der Server auch manuell gestartet werden:

    de ./target/ && ./budgetbutlerweb

Über ein Webbrowser kann die Webseite nun lokal erreicht werden:

    http://localhost:5000

## Updates

BudgetButlerWeb aktualisieren:

	# Code aktualisieren
	git pull

    # Anwendung neu bauen
    build.sh

## Softwaretests ausführen

Alle Softwaretests mit cargo starten:

    cd butler_offline
	cargo test

## Umgebungsvariablen

Wenn die Anwendung lokal auf dem Computer betrieben wird, müssen keine Umgebungsvariablen gesetzt werden.

Sollte die Anwendung im Netzwerk betrieben werden, können/müssen folgende Umgebungsvariablen gesetzt werden, damit die
Anwendung korrekt mit der Begleiter-App kommunizieren kann:

| Wert                      | Default   | Beschreibung                                      |
|---------------------------|-----------|---------------------------------------------------|
| BUDGETBUTLER_APP_ROOT     | localhost | Adresse, unter der die Anwendung erreichbar ist.  |
| BUDGETBUTLER_APP_PORT     | 5000      | Port, unter dem die Anwendung erreichbar ist.     |
| BUDGETBUTLER_APP_PROTOCOL | http      | Protokoll, unter dem die Anwendung erreichbar ist |

Werden hier Werte geändert, muss die Umgebungsvariable `ALLOWED_REDIRECTS` in der Begleiter-App entsprechend angepasst
werden, damit die lokale App sich bei der Begleiter-App anmelden kann.

## Betrieb mit Docker / Docker-Compose

* [Hier liegen gebaute Docker-Images](https://hub.docker.com/u/sebastianrzk),
  und [hier sind Deployment Beispiele zu finden](https://github.com/SebastianRzk/BudgetButlerWeb/tree/master/docker-compose-examples)

### Migration von Version 3.0.0 auf 4.0.0 (von Python Client auf Rust Client)

1. Cargo installieren
2. Daten automatisch mit migrieren (bitte <dein Nutzername> durch deinen Nutzername ersetzen)

   python database_migrator/main.py ./Database_<dein Nutzername>.csv