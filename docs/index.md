# BudgetButlerWeb
[![Build Status](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb.svg?branch=master)](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb) [![codecov](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb/branch/master/graph/badge.svg)](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb) (Broken: [![Coverage Status](https://coveralls.io/repos/github/RosesTheN00b/BudgetButlerWeb/badge.svg?branch=master)](https://coveralls.io/github/RosesTheN00b/BudgetButlerWeb?branch=master))

[Hauptsiete][index.md]
[Screenshots][screenshots.md]
[TODOs][todo.md]

## Idee

* Einfache Datenhaltung: Die Daten sind im CSV-Format gespeichert und damit mit einem Textverarbeitungsprogramm oder einem Tabellenverarbeitungsprogramm zugänglich.
* Schlankes Design
* Hohe Geschwindigkeit, auch bei großen Datenmengen
* Quelloffen

## Systeemvoraussetzungen

* Python 3.6
* Pip
* Moderner Webbrowser (z.B.. Firefox or Chromium)
* (git)

## Installation
Das Git-Repository clonen:

	git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

Ins Projektverzeichnis wechseln:

	cd BudgetButlerWeb

Abhängigkeiten mit pip installieren:

	pip install -r requirements.txt

## Starten

Im Projektverzeichnis in die Django-App navigieren und Django-Server starten:

	cd mysite
	python manage.py runserver

Webbrowser öffnen und folgende Url besuchen:

	http://127.0.0.1:8000/

## Updates

BudgetButlerWeb updaten:

	git pull

Mit pip-review die Abhängigkeiten aktualisieren:

	sudo pip-review --local --interactive



