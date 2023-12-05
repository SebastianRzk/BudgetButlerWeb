from butler_offline.views.einzelbuchungen.split_dauerauftrag import handle_request, SplitDauerauftraegeContext, index
from butler_offline.test.request_stubs import PostRequestAction
from butler_offline.core.database import Dauerauftraege
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.frequency import FREQUENCY_MONATLICH_NAME
from butler_offline.core.time import stub_today_with
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler


def test_preset_values_should_be_transactional():
    stub_today_with(datum('01.01.2023'))
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(
        startdatum=datum('01.01.2022'),
        endedatum=datum('02.01.2023'),
        rhythmus=FREQUENCY_MONATLICH_NAME,
        kategorie='kategorie123',
        name='name123',
        wert=123
    )
    context = SplitDauerauftraegeContext(dauerauftraege=dauerauftraege)

    result = handle_request(request=PostRequestAction(action='preset_values',
                                                      args={'dauerauftrag_id': 0}),
                            context=context)

    assert result.is_transactional()


def test_index_should_be_secured_by_requesthandler():
    def handle():
        index(request=PostRequestAction(action='preset_values',
                                        args={'dauerauftrag_id': 0}))

    result = run_in_mocked_handler(handle)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['einzelbuchungen/split_dauerauftrag.html']


def test_preset_values_should_be_add_preset_for_date_and_wert():
    stub_today_with(datum('01.01.2023'))
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(
        startdatum=datum('01.01.2022'),
        endedatum=datum('02.01.2023'),
        rhythmus=FREQUENCY_MONATLICH_NAME,
        kategorie='kategorie123',
        name='name123',
        wert=123
    )
    context = SplitDauerauftraegeContext(dauerauftraege=dauerauftraege)

    result = handle_request(request=PostRequestAction(action='preset_values',
                                                      args={'dauerauftrag_id': 0}),
                            context=context)

    assert result.get('datum') == [
        {'can_be_chosen': False,
         'datum': '2022-01-01',
         'datum_german': '01.01.2022'},
        {'can_be_chosen': True,
         'datum': '2022-02-01',
         'datum_german': '01.02.2022'},
        {'can_be_chosen': True,
         'datum': '2022-03-01',
         'datum_german': '01.03.2022'},
        {'can_be_chosen': True,
         'datum': '2022-04-01',
         'datum_german': '01.04.2022'},
        {'can_be_chosen': True,
         'datum': '2022-05-01',
         'datum_german': '01.05.2022'},
        {'can_be_chosen': True,
         'datum': '2022-06-01',
         'datum_german': '01.06.2022'},
        {'can_be_chosen': True,
         'datum': '2022-07-01',
         'datum_german': '01.07.2022'},
        {'can_be_chosen': True,
         'datum': '2022-08-01',
         'datum_german': '01.08.2022'},
        {'can_be_chosen': True,
         'datum': '2022-09-01',
         'datum_german': '01.09.2022'},
        {'can_be_chosen': True,
         'datum': '2022-10-01',
         'datum_german': '01.10.2022'},
        {'can_be_chosen': True,
         'datum': '2022-11-01',
         'datum_german': '01.11.2022'},
        {'can_be_chosen': True,
         'datum': '2022-12-01',
         'datum_german': '01.12.2022'},
        {'can_be_chosen': True,
         'datum': '2023-01-01',
         'datum_german': '01.01.2023'},
    ]
    assert result.get('wert') == 123
    assert result.get('dauerauftrag_id') == 0


def test_split_should_split():
    stub_today_with(datum('01.01.2023'))
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(
        startdatum=datum('01.01.2022'),
        endedatum=datum('02.01.2023'),
        rhythmus=FREQUENCY_MONATLICH_NAME,
        kategorie='kategorie123',
        name='name123',
        wert=123
    )
    context = SplitDauerauftraegeContext(dauerauftraege=dauerauftraege)

    handle_request(request=PostRequestAction(action='split',
                                             args={'dauerauftrag_id': 0,
                                                   'datum': '2022-04-01',
                                                   'wert': '234'}),
                   context=context)

    assert dauerauftraege.select().count() == 2
    assert dauerauftraege.get(0) == {'Endedatum': datum('31.03.2022'),
                                     'Kategorie': 'kategorie123',
                                     'Name': 'name123',
                                     'Rhythmus': 'monatlich',
                                     'Startdatum': datum('01.01.2022'),
                                     'Wert': 123.0,
                                     'index': 0}
    assert dauerauftraege.get(1) == {'Endedatum': datum('02.01.2023'),
                                     'Kategorie': 'kategorie123',
                                     'Name': 'name123',
                                     'Rhythmus': 'monatlich',
                                     'Startdatum': datum('01.04.2022'),
                                     'Wert': 234.0,
                                     'index': 1}
