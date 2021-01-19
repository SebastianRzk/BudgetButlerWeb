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
** Automatischer Import von Sparbuchungen, Order sowie gemeinsamen Buchungen


* Gemeinsame Buchungen
** Erfassen, Ändern, Löschen
** Abrechnung erstellen.
** Abrechnungen exportieren und importieren

* Sparen
** Erfassen, Ändern und Löschen von Sparkontos, Sparbuchungen, Depots, Depotwerte, Order, Order-Dauerauftraegen sowie Depotauszuege
** Sparen Übersicht:
*** Vergleich: Einnahmen, Ausgaben und Sparen über die Zeit
*** Zusammensetzung der Sparanlage

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
* composer + php 7.3+

### Systemanforderung für den Betrieb:

* Webspace mit PHP 7.3+
* Relationale Datenbank

oder:

* docker und docker-compose

### Installation Webspace

* Repo clonen

        git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

* Ins Projektverzeichnis wechseln

        cd BudgetButlerWeb

* Build in das Verzeichnis `butler_online_distribution` triggern

        sh butler_online_install/compose.sh

* Datenbank-Zugangsdaten in die Datei `butler_online_distribution/webspace_edition/api/db.ini` eintragen

* Für http (und nicht https Betrieb) in der Datei `api/util/creds.php` in der Methode `online` den Rückgabewert auf `false` ändern

* Diesen Ordner auf den Webspace laden `butler_online_distribution/webspace_edition`

* Prüfen, dass die Datei `db.ini` von außen nicht erreichbar ist.

* Login auf `/`. Initiale Anmeldedaten:
    * User: admin@admin.de
    * Password: adminadminadmin

### Installation docker + docker-compose

* Repo clonen

        git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

* Ins Projektverzeichnis wechseln

        cd BudgetButlerWeb

* Build in das Verzeichnis `butler_online_distribution` triggern

        sh butler_online_install/compose.sh

* In das Verzeichnis wechseln: `butler_online_distribution/docker_edition/budget_butler`

*  Gegebenenfalls die Passwörder in der `db.env` ändern

* Für http (und nicht https Betrieb) in der Datei `src/api/util/creds.php` in der Methode `online` den Rückgabewert auf `false` ändern

* Folgenden Befehl ausführen:

	docker-compose up

### Aktualisierven von docker-compose server

* Dateien aktualisieren `butler_online_install/compose_incremental.sh` docker-compose server neu bauen und starten: `docker-compose up -d --force-recreate --build`

* Login auf `/`. Initiale Anmeldedaten:
    * User: admin@admin.de
    * Password: adminadminadmin
