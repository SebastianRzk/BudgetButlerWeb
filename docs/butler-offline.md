---
layout: default
---

# Offline Anwendung: BudgetButlerWeb

## Menu

### Weitere Seiten

* [Hauptseite](index.md)
* [Companion-App](butler-companion)

### Inhaltsverzeichnis

* [Fachlicher Ansatz](#fachlicher-ansatz)
* [Systemvoraussetzungen](#systemvoraussetzungen)
* [Installation](#installation)
* [BudgetButlerWeb starten](#budgetbutlerweb-starten)
* [Updates](#updates)
* [Umgebungsvariablen](#umgebungsvariablen)
* [Betrieb mit Docker / Docker-Compose](#betrieb-mit-docker--docker-compose)
* [Migration von Version 3.0.0 auf 4.0.0 (von Python Client auf Rust Client)](#migration-von-version-300-auf-400-von-python-client-auf-rust-client)
* [Technischer Ansatz](#technischer-ansatz)

![Dashboard](img/screenshots_desktop/dashboard.png)

## Fachlicher Ansatz

### Datenmodell

BudgetButlerWeb unterscheidet im Wesentlichen 2 verschiedene Buchungstypen:

* **Statische / nicht-dynamische Buchungen**: Buchungen, welche einzeln erfasst werden und keine Verbindung zu anderen
  Buchungen haben. Alle Entitäten, welche in der CSV-Datei auf der Platte gespeichert sind, gehören dieser Gruppe an.
* **Dynamsiche Buchungen**: Buchungen, welche nicht direkt angelegt werden, sondern sich aus anderen statischen oder
  dynamischen Buchungen ergeben. Beispielsweise die einzelnen Buchungen eines Dauerauftrags, oder eine Ausgabe vom
  Typ "Sparen", welche automatisch durch eine Wertpapier-Order angelegt wird. Diese Buchungen werden nicht gespeichert,
  sondern immer wieder zur Laufzeit neu berechnet. Dies ermöglicht, dass kaskadierende Buchungs-Folgen, wie
  beispielsweise ein Wertpapier-Dauerauftrag, welcher einzelne Order-Buchungen erzeugt, welche ihrerseits wieder
  einzelne Ausgaben erzeugen auch nachträglich angepasst werden können.

Folgende Entitäten können erfasst werden:

**Einzelbuchungen**

| Entität       | Beschreibung                                                       |
|---------------|--------------------------------------------------------------------|
| Einzelbuchung | Einnahmen und Ausgaben, welche einmalig oder unregelmäßig anfallen |
| Dauerauftrag  | Wiederkehrende Einnahmen oder Ausgaben                             |

**Gemeinsame Buchungen**

| Entität            | Beschreibung                                                                                                                               |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Gemeinsame Buchung | Gemeinsame Einnahmen oder Ausgaben, jeweils einer Person zugeordnet                                                                        |
| Abrechnung         | Abrechnung von gemeinsamen Ausgaben, wird erstellt wenn gemeinsame Buchungen abgerechnet, und somit in Einzelbuchungen umgewandelt werden. |

**Sparen**

| Entität            | Beschreibung                                                                                             |
|--------------------|----------------------------------------------------------------------------------------------------------|
| Konto              | Ein Konto oder Depot, auf welchem gespart wird                                                           |
| Sparbuchung        | Einzahlung, Auszahlung, Erfassung von Kosten und Zinsen auf Konto-Ebene.                                 |
| Order              | Kauf oder Verkauf von Wertpapieren, Erfassung von Kosten oder Erträgen auf Wertpapier-Ebene              |
| Order-Dauerauftrag | Wiederkehrende Order, welche einzelne Order-Buchungen erzeugen                                           |
| Depotwert          | Etwas, was in einem Depot bespart werden kann. Wertpapiere, ETF, Kryptowährungen o.ä.                    |
| Depotauszug        | Wert von Depotwerten in einem Depot, zu einem bestimmten Zeitpunkt.                                      |

Folgende Buchungen führen zu dynamischen Buchungen:

| Buchungstyp                                              | Erzeugte Buchungen                                    | 
|----------------------------------------------------------|-------------------------------------------------------|
| Dauerauftrag                                             | erzeugt Einzelbuchungen, also Ausgaben oder Einnahmen |
| Sparbuchung (z.B. Überweisung von Geld auf ein Sparbuch) | erzeugt Einzelbuchungen mit der Kategorie "Sparen"    |
| Order (z.B. Kauf oder Verkauf von Wertpapieren)          | erzeugt Einzelbuchungen mit der Kategorie "Sparen"    |
| Order-Dauerauftrag                                       | erzeugt einzelne Order                                |

### Zusammenarbeit mit der Begleiter-App

Die Begleiter-App ist eine Web-App, welche auf mobilen Geräten genutzt werden kann. Sie ermöglicht das Erfassen von
Buchungen unterwegs.
Sie kann mit der Offline-Anwendung kommunizieren, um Buchungen zu importieren, welche auf dem mobilen Gerät erfasst
wurden. Importierte Buchungen werden im Anschluss automatisch aus der Begleiter-App gelöscht.

Eine Übertragung von Daten aus der Offline-Anwendung in die Begleiter-App ist eigentlich nicht vorgesehen. Für gemeinsame
Buchungen, welche noch nicht abgerechnet wurden, ist dies dennoch möglich. Weiterführend können auch die bestehenden
Kategorien aus der Desktop-Anwendung die Begleiter-App importiert werden.

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

    cd ./target/ && ./budgetbutlerweb

Über einen Webbrowser kann die Webseite nun lokal erreicht werden:

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
    * `src/main.rs`: Hauptdatei der Anwendung, welche den Webserver startet, die Routen in Form von Methoden einhängt und das
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
