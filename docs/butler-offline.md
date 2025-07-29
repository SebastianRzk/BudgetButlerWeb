---
layout: base.njk
title: Butler Offline Anwendung - BudgetButlerWeb
---

# Offline Anwendung: BudgetButlerWeb

<img src="{{config.pathPrefix}}img/screenshots_desktop/dashboard.png" alt="Dashboard"/>

## Installation in Arch Linux mittels AUR

Das Paket `budgetbutlerweb-desktop` installieren und die Applikation über den Befehl`budgetbutlerweb` oder über das
Anwendungsicon starten.

## Installation in Arch Linux mittels PKGBUILD

1. Das Repository klonen und in das Verzeichnis wechseln:
   `git clone https://github.com/SebastianRzk/BudgetButlerWeb && cd BudgetButlerWeb`
2. Das Paket bauen `makepkg`
3. Das Paket installieren `sudo pacman -U budgetbutlerweb-desktop-*.pkg.tar.zst`
4. Anwendung über das Anwendungsicon starten oder über den Befehl `budgetbutlerweb`.

## Installation mit docker / docker-compose

### Nutzung von fertigem Image aus Docker-Hub

Mithilfe von github-actions werden automatisch docker-images gebaut und in docker-hub gepublished.

Wie die Anwendung am besten in Docker konfiguriert wird, kann
dem <a href="https://github.com/SebastianRzk/BudgetButlerWeb/blob/master/docker-compose-examples/budget_butler_desktop/docker-compose.yml">
docker-compose.yml</a> aus dem Ordner
<a href="https://github.com/SebastianRzk/BudgetButlerWeb/tree/master/docker-compose-examples/budget_butler_desktop~~~~">
docker-compose-examples/budget_butler_desktop</a> entnommen werden.

Für `x86_64` kann das tag `latest` verwendet werden, für `arm64` das tag `latest-arm64` (siehe
auch [Docker-Hub](https://hub.docker.com/r/sebastianrzk/budgetbutlerweb-desktopapp/tags)).

### Selbst gebautes Docker-Image

Neben dem fertigen Image kann die Anwendung auch selbst gebaut werden.

Im
Ordner <a href="https://github.com/SebastianRzk/BudgetButlerWeb/tree/master/docker-compose-examples/budget_butler_desktop_local_build">
docker-compose-examples/budget_butler_desktop_local_build</a> befindet sich ein shell-script, welches ein
Docker-Image baut und das danebenliegende `docker-compose.yml` startet.

## Manuelle Installation (Linux, mit Anpassungen aber auch für Windows und MacOS)

### Systemvoraussetzungen

* Rust / Cargo
* Versionierung: git
* Anwendungsicon sowie Startup-Skript: shell und npm (für Electron-Client)
* Falls nicht der Electron-Client verwendet wird: Webbrowser (z.B. Firefox oder Chromium)

### Installation

Das Git-Repository klonen:

    ```sh
	git clone https://github.com/SebastianRzk/BudgetButlerWeb.git
    ```

Ins Projektverzeichnis wechseln:

    ```sh
	cd BudgetButlerWeb
    ```

Anwendung bauen

    ```sh
    sh build.sh
    ```

Optional: Anwendungsicon anlegen:

    ```sh
    sh create_desktop_shortcut.sh
    ```

### BudgetButlerWeb starten

Die Applikation kann über das Anwendungsicon gestartet werden

Alternativ kann der Electron Client manuell gestartet werden, dieser startet das Rust-Backend automatisch und stoppt
dieses, wenn das Fenster geschlossen wird.

    ```sh
	cd ./target/ && ./application-wrapper/budgetbutlerweb
    ```

Alternativ kann der Server auch manuell gestartet werden:

    ```sh
    cd ./target/ && ./budgetbutlerweb
    ```

Über einen Webbrowser kann die Webseite nun lokal erreicht werden:

    ```sh
    http://localhost:5000
    ```

### Updates

BudgetButlerWeb aktualisieren:

```
# Code aktualisieren
git pull

# Anwendung neu bauen
build.sh
```

### Softwaretests ausführen

Alle Softwaretests mit cargo starten:

    ```sh
    cd butler_offline
	cargo test
    ```

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

    ```sh
       python database_migrator/main.py ./Database_#dein Nutzername#.csv
    ```

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

### Erweiterung des ISIN-Datensatzes für die Depot-Analyse

Der ISIN-Datensatz wird im
Projekt [BudgetButlerWeb-ISIN-Data](https://github.com/SebastianRzk/BudgetButlerWeb-ISIN-Data) verwaltet und kann dort
erweitert werden.

### Bekannte Probleme / Herausforderungen

#### Allgemein

* Die Anwendung ist aktuell nur in deutscher Sprache verfügbar
* Die Anwendung ist aktuell nur für Linux getestet
* Die Anwendung ist aktuell nur für `x86_64` getestet

#### Spezifisch

##### 1. Das Starten der Applikation bricht mit folgender Meldung ab:

```
 Gtk-ERROR **: 21:57:46.125: GTK 2/3 symbols detected. Using GTK 2/3 and GTK 4 in the same process is not supported
/usr/bin/budgetbutlerweb: Zeile 3:  4649 Trace/Breakpoint ausgelöst   (Speicherabzug geschrieben) electron /usr/share/budgetbutlerweb/app.asar --installed "$@"
```

Lösung: Warten auf eine neue Electron Version (36.2.1 ist nicht kompatibel mit GTK 4.0+)

Work-Around: Electron Version <= 35.0 verwenden. Also beispielsweise das Paket `electron-35.0.0` installieren, und in
der Datei `/usr/share/budgetbutlerweb/budgetbutlerweb` die Zeile `electron ...` durch `electron35 ...` ersetzen.

##### 2. Das Bauen der Applikation bricht mit folgender Fehlermeldung ab:

```
An unhandled rejection has occurred inside Forge:
Error [ERR_MODULE_NOT_FOUND]: 
1. Cannot find module '/tmp/test/my-app/webpack.main.config' imported from /tmp/test/my-app/forge.config.ts
2. Cannot find module '/tmp/test/my-app/webpack.main.config' imported from /tmp/test/my-app/forge.config.ts
at finalizeResolution (node:internal/modules/esm/resolve:275:11)
```

Lösung: BudgetButlerWeb auf die aktuelle Version aktualisieren.

Work-Around: Node-Version <= 23.5 verwenden (
siehe [Bug bei Electron Forge](https://github.com/electron/forge/issues/3872))