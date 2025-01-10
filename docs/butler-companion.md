# Begleiter Web-App

## Menu

### Weitere Seiten

* [Hauptseite](index.md)
* [Desktop-Anwendung](butler-offline.md)

### Inhaltsverzeichnis

* [Build](#build)
* [Betrieb](#betrieb)

### Build

#### Anforderungen zum Build

#### Build in der Entwicklungsumgebung

Systemanforderungen:

* npm
* rust und mysql library (z.B. MariaDB)

Vorgehen:

* Frontend:

    * In das Verzeichnis `butler_online/budgetbutler` wechseln
    * Mit `npm install` fehlende Abhängigkeiten installieren
    * Angular-Build anstoßen `npm run build -- --configuration=production`

* Backend:

    * In das Verzeichnis `butler_online_api` wechseln
    * Rust-Build anstoßen `cargo build --release`

oder:

Systemanforderungen:

* docker (und docker-compose)

Vorgehen:

* In das Verzeichnis `butler_online_distribution/budget_butler_local_build` wechseln
* Build-Skript ausführen: `sh build_and_run_it.sh`

### Betrieb

Systemanforderungen für den Betrieb:

* docker und docker-compose

Ein Beispiel-Docker-Compose-File kann in `butler_online_distribution/budget_butler` eingesehen werden.
Für den Betrieb müssen in `api.env` sowie in `db.env` Parameter beispielsweise für den OAuth-Flow ergänzt werden.

#### Besonderheit: Desktop-Client befindet sich im Netzwerk

Dann muss die Adresse des Servers über die Umgebungsvariable `ALLOWED_REDIRECTS` zusätzlich für die lokale
Authentifizierung freigegeben werden

* Beispiel für Nutzung der Desktop-Applikation ausschließlich im Netzwerk: `ALLOWED_REDIRECTS=http://meinlokale.domain.internal`
* Beispiel für parallele Nutzung zwischen Desktop-Applikation auf dem Rechner und im Netzwerk: `ALLOWED_REDIRECTS=http://localhost:5000,http://meinlokale.domain.internal`

