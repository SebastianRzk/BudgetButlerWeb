---
layout: default
---

# Offline Anwendung: BudgetButlerWeb

## Menu

### Weitere Seiten

* [Hauptseite / Idee und Motivation](index.md)
* [Idee und fachlicher Ansatz](fachlicher-ansatz.md)
* [Begleiter App / Webseite](butler-companion)

### Inhaltsverzeichnis

* [Installation in Arch Linux mittels AUR](#installation-in-arch-linux-mittels-aur)
* [Installation in Arch Linux mittels PKGBUILD](#installation-in-arch-linux-mittels-pkgbuild)
* [Manuelle Installation (Linux, mit Anpassungen aber auch für Windows und MacOS)](#manuelle-installation-linux-mit-anpassungen-aber-auch-für-windows-und-macos)
	* [Systemvoraussetzungen](#systemvoraussetzungen)
	* [BudgetButlerWeb starten](#budgetbutlerweb-starten)
* [Updates](#updates)
* [Umgebungsvariablen](#umgebungsvariablen)
* [Betrieb mit Docker / Docker-Compose](#betrieb-mit-docker--docker-compose)
* [Migration von Version 3.0.0 auf 4.0.0 (von Python Client auf Rust Client)](#migration-von-version-300-auf-400-von-python-client-auf-rust-client)
* [Technischer Ansatz](#technischer-ansatz)

![Dashboard](img/screenshots_desktop/dashboard.png)


## Installation in Arch Linux mittels AUR

Das Paket `budgetbutlerweb-desktop` installieren und die Applikation über den Befehl`budgetbutlerweb` oder über das
Anwendungsicon starten.

## Installation in Arch Linux mittels PKGBUILD

1. Das Repository klonen und in das Verzeichnis wechseln:
   `git clone https://github.com/SebastianRzk/BudgetButlerWeb && cd BudgetButlerWeb`
2. Das Paket bauen `makepkg`
3. Das Paket installieren `sudo pacman -U budgetbutlerweb-desktop-git-*.pkg.tar.zst`
4. Anwendung über das Anwendungsicon starten oder über den Befehl `budgetbutlerweb`.

## Manuelle Installation (Linux, mit Anpassungen aber auch für Windows und MacOS)

### Systemvoraussetzungen

* Rust / Cargo
* Versionierung: git
* Anwendungsicon sowie Startup-Skript: shell und npm (für Electron-Client)
* Falls nicht der Electron-Client verwendet wird: Webbrowser (z.B. Firefox oder Chromium)

### Installation

Das Git-Repository klonen:

	git clone https://github.com/SebastianRzk/BudgetButlerWeb.git

Ins Projektverzeichnis wechseln:

	cd BudgetButlerWeb

Anwendung bauen

    sh build.sh

Optional: Anwendungsicon anlegen:

    sh create_desktop_shortcut.sh

### BudgetButlerWeb starten

Die Applikation kann über das Anwendungsicon gestartet werden

Alternativ kann der Electron Client manuell gestartet werden, dieser startet das Rust-Backend automatisch und stoppt
dieses, wenn das Fenster geschlossen wird.

	cd ./target/ && ./application-wrapper/budgetbutlerweb

Alternativ kann der Server auch manuell gestartet werden:

    cd ./target/ && ./budgetbutlerweb

Über einen Webbrowser kann die Webseite nun lokal erreicht werden:

    http://localhost:5000

### Updates

BudgetButlerWeb aktualisieren:

	# Code aktualisieren
	git pull

    # Anwendung neu bauen
    build.sh

### Softwaretests ausführen

Alle Softwaretests mit cargo starten:

    cd butler_offline
	cargo test

### Umgebungsvariablen

Wenn die Anwendung lokal auf dem Computer betrieben wird, müssen keine Umgebungsvariablen gesetzt werden.

Sollte die Anwendung im Netzwerk betrieben werden, können/müssen folgende Umgebungsvariablen gesetzt werden, damit die
Anwendung korrekt mit der Begleiter-App kommunizieren kann:

| Wert                      | Default   | Beschreibung                                      |
|---------------------------|-----------|---------------------------------------------------|
| BUDGETBUTLER_APP_ROOT     | localhost | Adresse, unter der die Anwendung erreichbar ist.  |
| BUDGETBUTLER_APP_PORT     | 5000      | Port, unter dem die Anwendung erreichbar ist.     |
| BUDGETBUTLER_APP_PROTOCOL | http      | Protokoll, unter dem die Anwendung erreichbar ist |

Werden hier Werte geändert, muss die Umgebungsvariable `ALLOWED_REDIRECTS` in der Begleiter-App entsprechend angepasst
werden, damit sich die lokale App bei der Begleiter-App anmelden kann.

## Betrieb mit Docker / Docker-Compose

[Hier liegen gebaute Docker-Images](https://hub.docker.com/u/sebastianrzk)
und [hier sind Deployment Beispiele zu finden](https://github.com/SebastianRzk/BudgetButlerWeb/tree/master/docker-compose-examples).

### Migration von Version 3.0.0 auf 4.0.0 (von Python Client auf Rust Client)

1. Cargo installieren
2. Daten automatisch mit migrieren (bitte #dein Nutzername# durch deinen Nutzernamen ersetzen)

       python database_migrator/main.py ./Database_#dein Nutzername#.csv

## Technischer Ansatz

### Technologie

Die Offline-Anwendung ist ein Server, welcher die Datenhaltung und die Logik der Anwendung übernimmt und eine Oberfläche
in Form einer Webseite bereitstellt.
Diese Webseite wird mittels Electron in eine Desktop-Anwendung umgewandelt. Theoretisch ist es auch möglich, die
Webseite in einem Webbrowser zu öffnen und BudgetButlerWeb dort ohne Einschränkung zu Nutzen.

Maßgebliche Technologien:

* [actix-web](https://actix.rs/) als Webserver
* [askama](https://github.com/rinja-rs/askama) als Template-Engine (ähnlich
  wie [Jinja2](https://jinja.palletsprojects.com/))
* [electron-forge](https://www.electronforge.io/) als Desktop-Client

### Struktur

Die Anwendung befindet sich in `butler_offline`.

Hier sind die folgenden Verzeichnisse zu finden:

* `src/`: Rust-Quelltext der Anwendung
	* `src/main.rs`: Hauptdatei der Anwendung, welche den Webserver startet, die Routen in Form von Methoden einhängt
	  und das
	  initiale Setup durchführt
	* `src/budgetbutler`: Fachlicher Quelltext
	* `src/io`: Ein- und Ausgabe der Anwendung, beispielsweise für das Lesen und Schreiben von CSV-Dateien, oder für das
	  Rendern von HTML-Dateien
	* `src/model`: Datenmodell der Anwendung
* `templates/`: HTML-Dateien, welche mittels `askama` in die Webseite eingebunden werden
* `static/`: Statische Dateien, wie CSS-Dateien, Schriftarten, Bilder und JavaScript-Dateien

Die Anwendung kann mittels `cargo run` gestartet werden. Der Webserver ist dann unter `http://localhost:5000`
erreichbar.

In `application-wrapper` befindet sich der Electron-Client. Dieser startet die Rust-Anwendung und öffnet ein Fenster, in
dem die Webseite angezeigt wird.
