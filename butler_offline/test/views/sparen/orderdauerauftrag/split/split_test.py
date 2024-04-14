from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.core.frequency import FREQUENCY_MONATLICH_NAME
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.views.sparen.orderdauerauftrag.split import (get_ausführungszeitpunkte_fuer_orderdauerauftrag,
                                                                 split_dauerauftrag)


def test_berechne_moegliche_ausfuehrungszeitpunkte_should_cap_on_5_in_der_zukunft():
    dauerauftraege = OrderDauerauftrag()
    dauerauftraege.add(
        startdatum=datum('01.01.2022'),
        endedatum=datum('31.12.2099'),
        name='name123',
        depotwert='depotwert123',
        konto='konto123',
        rhythmus=FREQUENCY_MONATLICH_NAME,
        wert=123
    )

    result = get_ausführungszeitpunkte_fuer_orderdauerauftrag(orderdauerauftraege=dauerauftraege,
                                                              orderdauerauftrag_id=0,
                                                              today=datum('02.01.2022'))

    assert result == [
        datum('01.01.2022'),
        datum('01.02.2022'),
        datum('01.03.2022'),
        datum('01.04.2022'),
        datum('01.05.2022'),
        datum('01.06.2022'),
    ]


def test_berechne_moegliche_ausfuehrungszeitpunkte_should_cap_at_endedatum():
    dauerauftraege = OrderDauerauftrag()
    dauerauftraege.add(
        startdatum=datum('01.01.2022'),
        endedatum=datum('02.03.2022'),
        name='name123',
        depotwert='depotwert123',
        konto='konto123',
        rhythmus=FREQUENCY_MONATLICH_NAME,
        wert=123
    )

    result = get_ausführungszeitpunkte_fuer_orderdauerauftrag(orderdauerauftraege=dauerauftraege,
                                                              orderdauerauftrag_id=0,
                                                              today=datum('02.01.2022'))

    assert result == [
        datum('01.01.2022'),
        datum('01.02.2022'),
        datum('01.03.2022'),
    ]


def test_split():
    dauerauftraege = OrderDauerauftrag()
    dauerauftraege.add(
        startdatum=datum('01.01.2022'),
        endedatum=datum('02.01.2023'),
        name='name123',
        depotwert='depotwert123',
        konto='konto123',
        rhythmus=FREQUENCY_MONATLICH_NAME,
        wert=123
    )

    split_dauerauftrag(orderdauerauftraege=dauerauftraege,
                       split_date=datum('01.03.2022'),
                       wert=234,
                       orderdauerauftrag_id=0)

    assert dauerauftraege.select().count() == 2
    assert dauerauftraege.get(0) == {
        'Startdatum': datum('01.01.2022'),
        'Endedatum': datum('28.02.2022'),
        'Name': 'name123',
        'Depotwert': 'depotwert123',
        'Konto': 'konto123',
        'Rhythmus': FREQUENCY_MONATLICH_NAME,
        'Wert': 123,
        'index': 0
    }
    assert dauerauftraege.get(1) == {
        'Startdatum': datum('01.03.2022'),
        'Endedatum': datum('02.01.2023'),
        'Name': 'name123',
        'Depotwert': 'depotwert123',
        'Konto': 'konto123',
        'Rhythmus': FREQUENCY_MONATLICH_NAME,
        'Wert': 234,
        'index': 1
    }
