# BudgetButlerWeb
[![Build Status](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb.svg?branch=master)](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb) [![codecov](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb/branch/master/graph/badge.svg)](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb)

* TOC 
{:toc}

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
** Einzelbuchungen (erfassen, ändern, löschen)
** Daueraufträge (erfassen, ändern, löschen)
** Monatsübersicht
** Jahresübersicht


* Gemeinsame Buchungen
** Erfassen, Ändern, Löschen
** Abrechnung erstellen.
** Abrechnungen exportieren und importieren

* Konfiguration
** Farbthema anpassen
** Farben der Kategorien anpassen
** Verwendung mehrerer Datenbanken

## Offline Anwendung: BudgetButlerWeb

### Systemvoraussetzungen

* Python 3.6
* Pip
* Moderner Webbrowser (z.B. Firefox oder Chromium)
* Startup-Skript: shell, curl, Chromium
* Versionierung: git

### Installation
Das Git-Repository clonen:

	git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

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

## Begleiter Web-App:

### Systemanfoderungen zum Build

* npm
* composer

### Systemanforderung für den Betrieb:

* Webspace mit PHP
* Relationale Datenbank

### Installation

* Repo clonen

        git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

* Ins Projektverzeichnis wechseln

        cd BudgetButlerWeb

* Build in das Verzeichnis `butler_online_distribution` triggern

        sh butler_online_install/compose.sh

* Datenbank-Zugangsdaten in die Datei `butler_online_distribution/api/db.ini` eintragen

* Diesen Ordner auf den Webspace laden `butler_online_distribution`

* Diese SQL-Skripte in der Datenbank ausführen `butler_online_install/`

* Prüfen, dass die Datei `db.ini` von außen nicht erreichbar ist.

* Login auf `/`. Initiale Anmeldedaten:
    * User: admin@admin.de
    * Password: adminadminadmin


