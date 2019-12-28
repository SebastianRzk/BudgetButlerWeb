# BudgetButlerWeb
[![Build Status](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb.svg?branch=master)](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb) [![codecov](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb/branch/master/graph/badge.svg)](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb)

* TOC {:toc}

## Idee

* Einfache Datenhaltung: Die Daten sind im CSV-Format gespeichert und damit mit einem Textverarbeitungsprogramm oder einem Tabellenverarbeitungsprogramm zugänglich.
* Schlankes Design
* Hohe Geschwindigkeit, auch bei großen Datenmengen
* Quelloffen
* Individualisierbar

## Merkmale

* Monatsübersicht
* Jahresübersicht
* Einzelbuchungen (erfassen, ändern, löschen)
* Daueraufträge (erfassen, ändern, löschen)
* Gemeinsame Buchungen (erfassen, ändern, löschen, abrechnen, aus Abrechnung importieren)
* Farbthema anpassen
* Farben der Kategorien anpassen
* Verwendung mehrerer Datenbanken

## Offline Anwendung

### Systemvoraussetzungen

* Python 3.6
* Pip
* Moderner Webbrowser (z.B. Firefox oder Chromium)
* (git)

### Installation
Das Git-Repository clonen:

	git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

Ins Projektverzeichnis wechseln:

	cd BudgetButlerWeb

### Server Starten

Flask-Server starten:

	sh start_butler_offline.sh

Webbrowser öffnen und folgende Url besuchen:

	http://127.0.0.1:5000/
	
### Softwaretests ausführen

Alle Softwaretestsmit pytest starten:

	pytest

Testabdeckung mit pytest berechnen:

	pytest butler_offline --cov

### Updates

BudgetButlerWeb aktualisieren:

	git pull




