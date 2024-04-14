from datetime import date
from datetime import timedelta
from typing import List

from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.views.shared.wiederkehrend import get_ausfuehrungszeitpunkte


def split_dauerauftrag(
        orderdauerauftraege: OrderDauerauftrag,
        orderdauerauftrag_id: int,
        split_date: date,
        wert) -> None:
    endedatum_aenderung = split_date - timedelta(days=1)
    dauerauftrag_alt = orderdauerauftraege.get(db_index=orderdauerauftrag_id)
    endedatum_alt = dauerauftrag_alt['Endedatum']

    orderdauerauftraege.edit_element(index=orderdauerauftrag_id, new_element_map={'Endedatum': endedatum_aenderung})

    orderdauerauftraege.add(
        startdatum=split_date,
        endedatum=endedatum_alt,
        name=dauerauftrag_alt['Name'],
        depotwert=dauerauftrag_alt['Depotwert'],
        konto=dauerauftrag_alt['Konto'],
        rhythmus=dauerauftrag_alt['Rhythmus'],
        wert=wert
    )


def get_ausführungszeitpunkte_fuer_orderdauerauftrag(
        orderdauerauftraege: OrderDauerauftrag,
        orderdauerauftrag_id: int,
        today: date
) -> List[date]:
    dauerauftrag = orderdauerauftraege.get(orderdauerauftrag_id)
    return get_ausfuehrungszeitpunkte(
        rhythmus=dauerauftrag['Rhythmus'],
        today=today,
        start_datum=dauerauftrag['Startdatum'],
        ende_datum=dauerauftrag['Endedatum']
    )
