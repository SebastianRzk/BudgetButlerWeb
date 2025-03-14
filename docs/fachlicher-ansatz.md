---
layout: default
---

# Idee und fachlicher Ansatz

## Menu

### Weitere Seiten

* [Hauptseite / Idee und Motivation](index.md)
* [Desktop Anwendung](butler-offline.md)
* [Begleiter App / Webseite](butler-companion)

### Inhaltsverzeichnis

* [Datenmodell](#datenmodell)
* [Zusammenarbeit mit der Begleiter-App](#zusammenarbeit-mit-der-begleiter-app)

## Datenmodell

BudgetButlerWeb unterscheidet im Wesentlichen 2 verschiedene Buchungstypen:

* **Statische / nicht-dynamische Buchungen**: Buchungen, welche einzeln erfasst werden und keine Verbindung zu anderen
  Buchungen haben. Alle Entitäten, welche in der CSV-Datei auf der Platte gespeichert sind, gehören dieser Gruppe an.
* **Dynamsiche Buchungen**: Buchungen, welche nicht direkt angelegt werden, sondern sich aus anderen statischen oder
  dynamischen Buchungen ergeben. Beispielsweise die einzelnen Buchungen eines Dauerauftrags, oder eine Ausgabe vom
  Typ "Sparen", welche automatisch durch eine Wertpapier-Order angelegt wird. Diese Buchungen werden nicht gespeichert,
  sondern immer wieder zur Laufzeit neu berechnet. Dies ermöglicht, dass kaskadierende Buchungs-Folgen, wie
  beispielsweise ein Wertpapier-Dauerauftrag, welcher einzelne Order-Buchungen erzeugt, welche ihrerseits wieder
  einzelne Ausgaben erzeugen auch nachträglich angepasst werden können.

Folgende Entitäten können erfasst werden:

**Einzelbuchungen**

| Entität       | Beschreibung                                                       |
|---------------|--------------------------------------------------------------------|
| Einzelbuchung | Einnahmen und Ausgaben, welche einmalig oder unregelmäßig anfallen |
| Dauerauftrag  | Wiederkehrende Einnahmen oder Ausgaben                             |

**Gemeinsame Buchungen**

| Entität            | Beschreibung                                                                                                                               |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Gemeinsame Buchung | Gemeinsame Einnahmen oder Ausgaben, jeweils einer Person zugeordnet                                                                        |
| Abrechnung         | Abrechnung von gemeinsamen Ausgaben, wird erstellt wenn gemeinsame Buchungen abgerechnet, und somit in Einzelbuchungen umgewandelt werden. |

**Sparen**

| Entität            | Beschreibung                                                                                |
|--------------------|---------------------------------------------------------------------------------------------|
| Konto              | Ein Konto oder Depot, auf welchem gespart wird                                              |
| Sparbuchung        | Einzahlung, Auszahlung, Erfassung von Kosten und Zinsen auf Konto-Ebene.                    |
| Order              | Kauf oder Verkauf von Wertpapieren, Erfassung von Kosten oder Erträgen auf Wertpapier-Ebene |
| Order-Dauerauftrag | Wiederkehrende Order, welche einzelne Order-Buchungen erzeugen                              |
| Depotwert          | Etwas, was in einem Depot bespart werden kann. Wertpapiere, ETF, Kryptowährungen o.ä.       |
| Depotauszug        | Wert von Depotwerten in einem Depot, zu einem bestimmten Zeitpunkt.                         |

Folgende Buchungen führen zu dynamischen Buchungen:

| Buchungstyp                                              | Erzeugte Buchungen                                    | 
|----------------------------------------------------------|-------------------------------------------------------|
| Dauerauftrag                                             | erzeugt Einzelbuchungen, also Ausgaben oder Einnahmen |
| Sparbuchung (z.B. Überweisung von Geld auf ein Sparbuch) | erzeugt Einzelbuchungen mit der Kategorie "Sparen"    |
| Order (z.B. Kauf oder Verkauf von Wertpapieren)          | erzeugt Einzelbuchungen mit der Kategorie "Sparen"    |
| Order-Dauerauftrag                                       | erzeugt einzelne Order                                |

## Zusammenarbeit mit der Begleiter-App

Die Begleiter-App ist eine Web-App, welche auf mobilen Geräten genutzt werden kann. Sie ermöglicht das Erfassen von
Buchungen unterwegs.
Sie kann mit der Offline-Anwendung kommunizieren, um Buchungen zu importieren, welche auf dem mobilen Gerät erfasst
wurden. Importierte Buchungen werden im Anschluss automatisch aus der Begleiter-App gelöscht.

Eine Übertragung von Daten aus der Offline-Anwendung in die Begleiter-App ist eigentlich nicht vorgesehen. Für
gemeinsame Buchungen, welche noch nicht abgerechnet wurden, ist dies dennoch möglich. Weiterführend können auch die
bestehenden Kategorien aus der Desktop-Anwendung die Begleiter-App importiert werden.
