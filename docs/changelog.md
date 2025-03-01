---
layout: default
---

[zurück zur Übersicht](index.md)


## Inhalt

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
- Fix default-Selektion von Jahr auf der "Übersicht Einzelbuchungen" Seite, wenn die letzte Buchung nicht aus dem aktuellen Jahr ist

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