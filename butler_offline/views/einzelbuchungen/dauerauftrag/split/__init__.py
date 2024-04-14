from datetime import date
from datetime import timedelta
from typing import List

from butler_offline.core.database import Dauerauftraege
from butler_offline.views.shared.wiederkehrend import get_ausfuehrungszeitpunkte


def split_dauerauftrag(
        dauerauftraege: Dauerauftraege,
        dauerauftrag_id: int,
        split_date: date,
        wert) -> None:
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


def get_ausführungszeitpunkte_fuer_dauerauftrag(
        dauerauftraege: Dauerauftraege,
        dauerauftrag_id: int,
        today: date
    ) -> List[date]:
    dauerauftrag = dauerauftraege.get(dauerauftrag_id)
    return get_ausfuehrungszeitpunkte(
        rhythmus=dauerauftrag['Rhythmus'],
        today=today,
        start_datum=dauerauftrag['Startdatum'],
        ende_datum=dauerauftrag['Endedatum']
    )
