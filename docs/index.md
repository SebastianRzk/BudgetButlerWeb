# BudgetButlerWeb
[![Build Status](https://travis-ci.org/SebastianRzk/BudgetButlerWeb.svg?branch=master)](https://travis-ci.org/SebastianRzk/BudgetButlerWeb) [![codecov](https://codecov.io/gh/SebastianRzk/BudgetButlerWeb/branch/master/graph/badge.svg)](https://codecov.io/gh/SebastianRzk/BudgetButlerWeb)

* TOC
{:toc}

[Screenshots Desktop](screenshots_desktop)

[Screenshots Companion App](screenshots_mobile)

## Idee

* Einfache lokale Datenhaltung: Die Daten sind im CSV-Format gespeichert und damit mit einem Textverarbeitungsprogramm oder einem Tabellenverarbeitungsprogramm zugänglich.
* Unkomplizierte Einnahmen/Ausgaben-Rechnung, keine doppelte Buchführung.
* Schlanke Begleiter-Web-App für unterwegs (online-Version, mobil-optimiert). Import der Daten in die lokale Anwendung
* Schlankes Design
* Hohe Geschwindigkeit, auch bei großen Datenmengen
* Quelloffen
* Individualisierbar

## Merkmale

* Einzelbuchungen
  * Einzelbuchungen (erfassen, ändern, löschen)
  * Daueraufträge (erfassen, ändern, löschen)
  * Monatsübersicht
  * Jahresübersicht
  * Automatischer Import von Sparbuchungen, Order sowie gemeinsamen Buchungen


* Gemeinsame Buchungen
  * Erfassen, Ändern, Löschen
  * Abrechnung erstellen.
  * Abrechnungen exportieren und importieren


* Sparen
  * Erfassen, Ändern und Löschen von Sparkontos, Sparbuchungen, Depots, Depotwerte, Order, Order-Dauerauftraegen sowie Depotauszuege
  * Sparen Übersicht:
    * Vergleich: Einnahmen, Ausgaben und Sparen über die Zeit
    * Zusammensetzung der Sparanlage
  * ETF-Portfolio Vergleichen: Kosten, Sektoren und Länder jeweis pro ETF und nach Anteil im Portfolio


* Konfiguration
  * Farbthema anpassen
  * Farben der Kategorien anpassen
  * Verwendung mehrerer Datenbanken

## Offline Anwendung: BudgetButlerWeb

### Systemvoraussetzungen

* Python 3.9
* Pip
* Moderner Webbrowser (z.B. Firefox oder Chromium)
* Startup-Skript: shell, curl, Chromium
* Versionierung: git

### Installation
Das Git-Repository clonen:

	git clone https://github.com/SebastianRzk/BudgetButlerWeb.git

Ins Projektverzeichnis wechseln:

	cd BudgetButlerWeb

### Server Starten

Flask-Server starten:

	sh start_butler_offline.sh

BudgetButlerWeb ist unter folgender Adresse zu erreichen:

	http://127.0.0.1:5000/

### Softwaretests ausführen

Alle Softwaretestsmit pytest starten:

	pytest

Testabdeckung mit pytest berechnen:

	pytest butler_offline --cov

### Updates

BudgetButlerWeb aktualisieren:

	git pull


## Umgebungsvariablen
| Wert | Default | Beschreibung |
|------| ------- | ------------ |
| BUDGETBUTLERWEB_DATABASE_PATH | .. | Ordner an dem die Datenbanken gesucht werden sollen. |
| BUDGETBUTLERWEB_CONFIG_PATH | .. | Ordner an dem die Configuration gesucht werden soll. |

## Begleiter Web-App:

### Systemanfoderungen zum Build

* npm
* composer + php 7.3+

### Systemanforderung für den Betrieb:

* docker und docker-compose


### Installation docker + docker-compose

* Repo clonen

        git clone https://github.com/SebastianRzk/BudgetButlerWeb.git

* Ins Projektverzeichnis wechseln

        cd BudgetButlerWeb

* Für http (und nicht https Betrieb) in der Datei `butler_online_api/api/util/creds.php` in der Methode `online` den Rückgabewert auf `false` ändern

* Build in das Verzeichnis `butler_online_distribution` triggern

        sh butler_online_install/build_images.sh


* Folgenden Befehl ausführen `docker-compose up` in `butler_online_distribution/budget_butler`

* Login auf `/`. Initiale Anmeldedaten:
  * User: admin@admin.de
  * Password: adminadminadmin


