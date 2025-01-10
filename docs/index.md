# BudgetButlerWeb
![GithubCI Build and Test](https://github.com/SebastianRzk/BudgetButlerWeb/actions/workflows/build.yml/badge.svg?branch=master)
![GithubCI Publish](https://github.com/SebastianRzk/BudgetButlerWeb/actions/workflows/docker-to-docker-hub.yml/badge.svg?branch=master)

Ein einfaches haushaltsbuch für eine schlanke und individuelle Finanzverwaltung.

## Inhaltsverzeichnis

* [Idee](#idee)
* [Merkmale](#merkmale)
* [Mitmachen](#mitmachen)
* [Screenshots](#screenshots)
	* [Screenshots BudgetButlerWeb Offline Anwendung](#screenshots-budgetbutlerweb-offline-anwendung)
	* [Screenshots Begleiter Web-App](#screenshots-begleiter-web-app)
* [ :link: Desktop Client](butler-offline.md)
* [ :link: Begleiter Web-App](butler-companion.md)
* [ :link: Changelog](changelog.md)

## Idee

* Einfache lokale Datenhaltung: Die Daten sind im CSV-Format gespeichert und damit mit einem Textverarbeitungsprogramm
  oder einem Tabellenverarbeitungsprogramm zugänglich.
* Unkomplizierte Einnahmen/Ausgaben-Rechnung, keine doppelte Buchführung.
* Schlanke Begleiter-Web-App für unterwegs (online-Version, mobil-optimiert). Automatisierter Import der Daten in die
  lokale Anwendung
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
	* Abrechnungenpython database_migrator/main.py ./Database_Test_User.csv exportieren und importieren
	* Import von gemeinsame Buchungen aus der Begleiter Web-App


* Sparen
	* Erfassen, Ändern und Löschen von Sparkontos, Sparbuchungen, Depots, Depotwerte (mit Typ: ETF, Fond, Einzelaktie,
	  Crypto oder Robo), Order, Order-Daueraufträgen sowie Depotauszüge
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

## Mitmachen

* Fehler, Fragen, Anmerkungen oder Ideen gerne
  als ["ISSUE" hier hinterlassen](https://github.com/SebastianRzk/BudgetButlerWeb/issues)
* Code-Änderungen (Pull-Requests) immer bitte immer gegen den
  `dev`-[Branch hier hin](https://github.com/SebastianRzk/BudgetButlerWeb/pulls)
* [Hier liegt der blanke Code](https://github.com/SebastianRzk/BudgetButlerWeb)
* [Hier liegen die Docker-Images für die Begleiter Web-App](https://hub.docker.com/u/sebastianrzk),
  und [hier sind Deployment Beispiele für die Begleiter Web-App](https://github.com/SebastianRzk/BudgetButlerWeb/tree/master/docker-compose-examples)

## Screenshots

### Screenshots BudgetButlerWeb Offline Anwendung

<img src="img/screenshots_desktop/dashboard.png" alt="Dashboard" width="300"/>

#### Einzelbuchungen

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

### Screenshots Begleiter Web-App

<a href="img/screenshots_mobile/menu.png"><img src="img/screenshots_mobile/menu.png" alt="Dasboard" width="250"/></a>
<a href="img/screenshots_mobile/erfassen.png"><img src="img/screenshots_mobile/erfassen.png" alt="Dasboard" width="250"/></a>
<a href="img/screenshots_mobile/erfassen_desktop.png"><img src="img/screenshots_mobile/erfassen_desktop.png" alt="Dasboard" width="300"/></a>
<a href="img/screenshots_mobile/gemeinsam.png"><img src="img/screenshots_mobile/gemeinsam.png" alt="Dasboard" width="250"/></a>
<a href="img/screenshots_mobile/einzel.png"><img src="img/screenshots_mobile/einzel.png" alt="Dasboard" width="250"/></a>
<a href="img/screenshots_mobile/einzel.png"><img src="img/screenshots_mobile/erfassen_dauerauftrag.png" alt="Dasboard" width="250"/></a>
<a href="img/screenshots_mobile/einzel.png"><img src="img/screenshots_mobile/uebersicht_dauerauftrag.png" alt="Dasboard" width="250"/></a>

