# BudgetButlerWeb

[![Build Status](https://travis-ci.org/SebastianRzk/BudgetButlerWeb.svg?branch=master)](https://travis-ci.org/SebastianRzk/BudgetButlerWeb) [![codecov](https://codecov.io/gh/SebastianRzk/BudgetButlerWeb/branch/master/graph/badge.svg)](https://codecov.io/gh/SebastianRzk/BudgetButlerWeb)

## Dokumentation

[Webseite + Dokumentation](https://SebastianRzk.github.io/BudgetButlerWeb/)
<<<<<<< HEAD

## Umgebungsvariablen
| Wert | Default | Beschreibung |
|------| ------- | ------------ |
| DATABASE_PATH | /data (Docker) bzw. ".." (lokal) | Ordner an dem die Datenbanken gesucht werden sollen. |
| CONFIG_PATH | /data (Docker) bzw. ".." (lokal) | Ordner an dem die Configuration gesucht werden soll. |

## Beispiel Docker-Compose für Offline-App

```
budgetbutler_offline:
    environment:
      - 'DATABASE_PATH=/data'
      - 'CONFIG_PATH=/data'
      - 'TZ=${TZ}'
    image: 'dmkif/budgetbutler-offline:latest'
    ports: 
      - 5000:5000
    volumes:
      - '${USERDIR}/budgetbutler:/data'
```
=======
>>>>>>> 7e11c99eff7f25daab39d2ef594321b63ae2fa94
