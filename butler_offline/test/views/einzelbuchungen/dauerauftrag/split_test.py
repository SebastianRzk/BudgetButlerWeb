from butler_offline.views.einzelbuchungen.dauerauftrag.split import get_ausführungszeitpunkte, split_dauerauftrag
from butler_offline.core.database import Dauerauftraege
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.frequency import FREQUENCY_MONATLICH_NAME
from butler_offline.core.time import stub_today_with


def test_berechne_moegliche_ausfuehrungszeitpunkte_should_cap_on_5_in_der_zukunft():
    stub_today_with(datum('02.01.2022'))
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(
        startdatum=datum('01.01.2022'),
        endedatum=datum('31.12.2099'),
        name='',
        kategorie='',
        rhythmus=FREQUENCY_MONATLICH_NAME,
        wert=123
    )

    result = get_ausführungszeitpunkte(dauerauftraege=dauerauftraege,
                                       dauerauftrag_id=0)

    assert result == [
        datum('01.01.2022'),
        datum('01.02.2022'),
        datum('01.03.2022'),
        datum('01.04.2022'),
        datum('01.05.2022'),
        datum('01.06.2022'),
    ]


def test_berechne_moegliche_ausfuehrungszeitpunkte_should_cap_at_endedatum():
    stub_today_with(datum('02.01.2022'))
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(
        startdatum=datum('01.01.2022'),
        endedatum=datum('02.03.2022'),
        name='',
        kategorie='',
        rhythmus=FREQUENCY_MONATLICH_NAME,
        wert=123
    )

    result = get_ausführungszeitpunkte(dauerauftraege=dauerauftraege,
                                       dauerauftrag_id=0)

    assert result == [
        datum('01.01.2022'),
        datum('01.02.2022'),
        datum('01.03.2022'),
    ]


def test_split():
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(
        startdatum=datum('01.01.2022'),
        endedatum=datum('02.01.2023'),
        name='',
        kategorie='',
        rhythmus=FREQUENCY_MONATLICH_NAME,
        wert=123
    )

    split_dauerauftrag(dauerauftraege=dauerauftraege, split_date=datum('01.03.2022'), wert=234, dauerauftrag_id=0)

    assert dauerauftraege.select().count() == 2
    assert dauerauftraege.get(0) == {
        'Startdatum': datum('01.01.2022'),
        'Endedatum': datum('28.02.2022'),
        'Name': '',
        'Kategorie': '',
        'Rhythmus': FREQUENCY_MONATLICH_NAME,
        'Wert': 123,
        'index': 0
    }
    assert dauerauftraege.get(1) == {
        'Startdatum': datum('01.03.2022'),
        'Endedatum': datum('02.01.2023'),
        'Name': '',
        'Kategorie': '',
        'Rhythmus': FREQUENCY_MONATLICH_NAME,
        'Wert': 234,
        'index': 1
    }
