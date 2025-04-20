---
layout: default
---

[zurück zur Übersicht](index.md)

## Inhalt

- [v4.2.11 (2025-04-10)](#v4211-2025-04-10)
- [v4.2.10 (2025-03-31)](#v4210-2025-03-31)
- [v4.2.9 (2025-03-30)](#v429-2025-03-30)
- [v4.2.8 (2025-03-28)](#v428-2025-03-28)
- [v4.2.7 (2025-03-19)](#v427-2025-03-19)
- [v4.2.6 (2025-03-14)](#v426-2025-03-14)
- [v4.2.5 (2025-03-09)](#v425-2025-03-08)
- [v4.2.4 (2025-03-06)](#v424-2025-03-06)
- [v4.2.3 (2025-03-06)](#v423-2025-03-06)
- [v4.2.2 (2025-03-05)](#v422-2025-03-05)
- [v4.2.1 (2025-03-01)](#v421-2025-03-01)
- [v4.2.0 (2025-02-10)](#v420-2025-02-10)
- [v4.1.1 (2025-02-10)](#v411-2025-02-10)
- [v4.1.0 (2025-02-08)](#v410-2025-02-08)
- [v4.0.5 (2024-01-24)](#v405-2024-01-24)
- [v4.0.4 (2024-01-24)](#v404-2024-01-24)
- [v4.0.3 (2024-01-23)](#v403-2024-01-23)
- [v4.0.2 (2024-01-16)](#v402-2024-01-16)
- [v4.0.1 (2024-01-10)](#v401-2024-01-10)
- [v4.0.0 (2024-12-26)](#v400-2024-12-26)
- [v3.2.5 (2024-10-05)](#v325-2024-10-05)
- ...
- [v3.0.1 (2024-01-17)](#v301-2024-01-17)
- [v2.2.7 (2024-01-16)](#v227-2024-01-16)
- ...
- [v2.0.0 (2018-08-20)](#v200-2018-08-20)
- [v1.2.0 (2018-08-20)](#v120-2018-08-20)
- ...
- [v1.0.0 (2018-01-29)](#v100-2018-01-29)
- ...
- [v0.0.1 (2017-08-10)](#v001-2017-08-10)


### v4.3.0 ??

#### Änderungen Desktop-Client

* Feature: Ünterstützung neuer ETF-API [BudgetButlerWeb-ISIN-Data](https://github.com/SebastianRzk/BudgetButlerWeb-ISIN-Data)
* Fix Country-Codes mit Fußnoten
* Fix Gesamtkosten-Berechnung in ETF-Analyse

### v4.2.11 (2025-04-10)

#### Änderungen Desktop-Client

* Aktualisierung der Abhängigkeiten im Backend
* Aktualisierung der Abhängigkeiten im Application-Wrapper

#### Änderungen Begleiter-Web-App

* Aktualisierung der Abhängigkeiten im Backend
* Aktualisierung der Abhängigkeiten im Frontend

### v4.2.10 (2025-03-31)

#### Änderungen Desktop-Client

* Bugfix: Seitentitel werden korrekt im Browser / Fenster-Titel angezeigt

### v4.2.9 (2025-03-30)

#### Änderungen Desktop-Client

* Bugfix: Statische Ressourcen werden im Docker-Image der Desktop-App korrekt ausgeliefert


### v4.2.8 (2025-03-28)

#### Änderungen Desktop-Client

* Bugfix: Setzen von korrekter `StartupWMClass`, damit das Anwendungsfenster in der Taskleiste korrekt erkannt wird

#### Dokumentation

* Bugfix: Docker-compose Beispiel für die Begleiter-Web-App (mit Images aus Docker-Hub) korrigiert.
* Installations-Anleitungen weiter ausformuliert

### v4.2.7 (2025-03-19)

#### Änderungen Desktop-Client

* Korrigieren von Seiten-Überschriften im Sparen-Modul und Einzelbuchungen-Modul
* Interne Refactorings

### v4.2.6 (2025-03-14)

#### Änderungen Desktop-Client

* Fix von Clippy warnings
* Aktualisierung von Abhängigkeiten

#### Änderungen Begleiter-Web-App

* Auf den Übersichts-Seiten sind die Beträge nun rechtsbündig ausgerichtet

## v4.2.5 (2025-03-08)

### Änderungen Desktop-Client

* Aktualisierung der Abhängigkeiten von Rust-Backend
* Verbesserung von PKGBUILD

### Änderungen Begleiter-Web-App

* Aktualisierung der Abhängigkeiten im Backend

## v4.2.4 (2025-03-06)

### Änderungen Desktop-Client

- Aktualisieren von Pfad-Berechnung in der config.json. **Migration nötig**: Das Pfad-Präfix "data/" aus allen
  bestehenden Konfigurations-Pfaden entfernen.

## v4.2.3 (2025-03-06)

### Änderungen Begleiter App

- Aktualisierung der Abhängigkeiten im Frontend

## v4.2.2 (2025-03-05)

### Änderungen Desktop-Client

- Implementierung von Arch-Linux PKGBUILD

## v4.2.1 (2025-03-01)

### Änderungen Desktop-Client

- Config-JSON `pretty` speichern
- Internes Refactoring im Backend

### Änderungen Begleiter-Web-App

- Fix Menu-Button Einblendung
- Aktualisierung der Abhängigkeiten im Frontend
- Internes Refactoring im Frontend
- Internes Refactoring im Backend

## v4.2.0 (2025-02-10)

### Änderungen Desktop-Client

- Keine Änderungen

### Änderungen Begleiter-Web-App

- Übersicht-Seite um Gesamt-Betrag und Betrag nach Person erweitert

## v4.1.1 (2025-02-10)

### Änderungen Desktop-Client

- Keine Änderungen

### Änderungen Begleiter-Web-App

- Anpassung des Menu-Toggels

## v4.1.0 (2025-02-08)

### Änderungen Desktop-Client

- Arm64 docker-image
- Security Updates

### Änderungen Begleiter-Web-App

- Übersicht persönliche und gemeinsame Buchungen
- Buchungen können in der Erfassung geteilt werden
- Security Updates

## v4.0.5 (2024-01-24)

### Änderungen Desktop-Client

- Fix der Default-Selektion des Jahres in den Tabellenübersichten

### Änderungen Begleiter-Web-App

- Keine Änderungen

## v4.0.4 (2024-01-24)

### Änderungen Desktop-Client

- Fix von Betrag-Parsen mit unvollständigen Nachkommastellen
- Fix AddKategorie auf der "Gemeinsame Buchung hinzufügen" Seite
- Fix default-Selektion von Jahr auf der "Übersicht Einzelbuchungen" Seite, wenn die letzte Buchung nicht aus dem
  aktuellen Jahr ist

### Änderungen Begleiter-Web-App

- Hinzufügen von fehlendem Animations Modul

## v4.0.3 (2024-01-23)

### Änderungen Desktop-Client

- Aktualisierung von Rust-Backend
- Aktualisierung von Electron application-wrapper

### Änderungen Begleiter-Web-App

- Aktualisierung von Rust-Backend
- Aktualisierung von Angular-frontend

## v4.0.2 (2024-01-16)

### Änderungen Desktop-Client

- Beim Löschen von Einzelbuchungen verbleibt man auf der Seite des gleichen Jahrs
- Fix von Optimistic-Locking False-Positive beim Import
- Fix kleinerer Anzeigefehler

### Änderungen Begleiter-Web-App

- Keine Änderungen

## v4.0.1 (2024-01-10)

### Änderungen Desktop-Client

- Bereitstellung von Docker-Image und docker-compose.yml
- Erhöhung der Max-File-Size für Datei-Importe
- Fix Import von Abrechnungen mit "Gemeinsamen Buchungen"

### Änderungen Begleiter-Web-App

- "Authorisieren"-Dialog für die Offline-Anwendung enthält auch Möglichkeit zum Ablehnen
- Auch andere Domains als `localhost` können authorisiert werden (z.B. für Desktop-Client Netzwerkinstallation)

## v4.0.0 (2024-12-26)

### Änderungen Desktop-Client

- Reimplementierung in Rust
- Überarbeitung aller Oberflächen (v.a. Listen, Sparen, Sparbuchungen, Order)
- Manuelle Migration nötig (Migrationsskript in Repo)

### Änderungen Begleiter-Web-App

- Keine Änderungen

## v3.2.5 (2024-10-05)

### Änderungen Desktop-Client

- Keine Änderungen

### Änderungen Begleiter-Web-App

- Touch-Ui Inputs
- Montag ist erster Tag der Woche

## v3.0.1 (2024-01-17)

### Änderungen Desktop-Client

- Keine Änderungen

### Änderungen Begleiter-Web-App

- Erste Version mit Rust / Actix

## v2.2.7 (2024-01-16)

### Änderungen Desktop-Client

- Keine Änderungen

### Änderungen Begleiter-Web-App

- Letzte Version mit PHP FPM

## v2.0.0 (2018-08-20)

### Änderungen Desktop-Client

- Umbau von django -> flask (Verbesserung von Performance und Stabilität)

### Änderungen Begleiter-Web-App

- Deployment in docker
- Frontend in Angular

## v1.2.0 (2018-08-20)

### Änderungen Desktop-Client

- Anbindung von Begleiter-App

### Änderungen Begleiter-Web-App

- Erste Version (PHP)

## v1.0.0 (2018-01-29)

### Änderungen Desktop-Client

- Erste "fertige" Version

### Änderungen Begleiter-Web-App

- Keine Änderungen

## v0.0.1 (2017-08-10)

### Änderungen Desktop-Client

- Erstveröffentlichung (python / django)

### Änderungen Begleiter-Web-App

- Keine Änderungen
