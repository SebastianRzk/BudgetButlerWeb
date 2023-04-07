from typing import List
from datetime import date
from butler_offline.core.database import Dauerauftraege
from butler_offline.core.time import today
from butler_offline.core.frequency import get_function_for_name
from datetime import timedelta


def split_dauerauftrag(dauerauftraege: Dauerauftraege, dauerauftrag_id: int, split_date: date, wert) -> None:
    endedatum_aenderung = split_date - timedelta(days=1)
    dauerauftrag_alt = dauerauftraege.get(db_index=dauerauftrag_id)
    endedatum_alt = dauerauftrag_alt['Endedatum']

    dauerauftraege.edit_element(index=dauerauftrag_id, new_element_map={'Endedatum': endedatum_aenderung})

    dauerauftraege.add(
        startdatum=split_date,
        endedatum=endedatum_alt,
        name=dauerauftrag_alt['Name'],
        kategorie=dauerauftrag_alt['Kategorie'],
        rhythmus=dauerauftrag_alt['Rhythmus'],
        wert=wert
    )


def get_ausführungszeitpunkte(dauerauftraege: Dauerauftraege, dauerauftrag_id: int) -> List[date]:
    dauerauftrag = dauerauftraege.get(dauerauftrag_id)
    frequenz = get_function_for_name(dauerauftrag['Rhythmus'])
    auswahlzeitraum_ende = today() + frequenz(5)

    laufdatum = dauerauftrag['Startdatum']
    laufindex = 1
    ergebnis = []

    while laufdatum < auswahlzeitraum_ende and laufdatum < dauerauftrag['Endedatum']:
        ergebnis.append(laufdatum)

        laufdatum = dauerauftrag['Startdatum'] + frequenz(laufindex)
        laufindex += 1

    return ergebnis
