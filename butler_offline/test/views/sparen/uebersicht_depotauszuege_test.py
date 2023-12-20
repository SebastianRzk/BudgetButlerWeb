from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.test import assert_info_message_keine_depotauszuege_erfasst_in_context, \
    assert_keine_message_set
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.views.sparen import uebersicht_depotauszuege


def test_context_should_be_transactional():
    context = uebersicht_depotauszuege.handle_request(
        GetRequest(),
        context=get_test_data()
    )
    assert context.is_transactional()


def get_test_data():
    depotauszuege = Depotauszuege()
    depotauszuege.add(datum('01.01.2020'), '1isin', '1demokonto', 1)
    depotauszuege.add(datum('03.01.2020'), '2isin', '2demokonto', 2)
    depotauszuege.add(datum('03.01.2020'), '3isin', '2demokonto', 3)
    depotauszuege.add(datum('03.01.2020'), '4isin', '3demokonto', 4)
    print(depotauszuege.content)

    depotwerte = Depotwerte()
    depotwerte.add(name='1name', isin='1isin', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='2name', isin='2isin', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='3name', isin='3isin', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='4name', isin='4isin', typ=depotwerte.TYP_ETF)

    return uebersicht_depotauszuege.UebersichtDepotauszuegeContext(
        depotauszuege=depotauszuege,
        depotwerte=depotwerte
    )


def test_init_with_empty_database():
    context = uebersicht_depotauszuege.handle_request(
        GetRequest(),
        context=uebersicht_depotauszuege.UebersichtDepotauszuegeContext(
            depotauszuege=Depotauszuege(),
            depotwerte=Depotwerte()
        )
    )
    assert context.get('gesamt') == []
    assert_info_message_keine_depotauszuege_erfasst_in_context(context)


def test_init_filled_database():
    content = uebersicht_depotauszuege.handle_request(
        GetRequest(),
        context=get_test_data()
    )

    assert content.get('gesamt') == [
        {'buchungen': [
            {'depotwert': '1name (1isin)', 'wert': 1}],
            'index': 0,
            'name': '1demokonto vom 01.01.2020'},
        {'buchungen': [{'depotwert': '2name (2isin)', 'wert': 2},
                       {'depotwert': '3name (3isin)', 'wert': 3}],
         'index': 1,
         'name': '2demokonto vom 03.01.2020'},
        {'buchungen': [{'depotwert': '4name (4isin)', 'wert': 4}],
         'index': 3,
         'name': '3demokonto vom 03.01.2020'},
    ]
    assert_keine_message_set(content)


def test_delete():
    context = get_test_data()
    uebersicht_depotauszuege.handle_request(
        PostRequest({'action': 'delete', 'delete_index': '1'}),
        context=context
    )

    assert context.depotauszuege().select().count() == 2

    page_conent = uebersicht_depotauszuege.handle_request(
        GetRequest(),
        context=context)
    assert page_conent.get('gesamt') == [
        {'buchungen': [
            {'depotwert': '1name (1isin)', 'wert': 1}],
            'index': 0,
            'name': '1demokonto vom 01.01.2020'},
        {'buchungen': [{'depotwert': '4name (4isin)', 'wert': 4}],
         'index': 3,
         'name': '3demokonto vom 03.01.2020'},
    ]


def test_index_should_be_secured_by_request_handler():
    def index():
        uebersicht_depotauszuege.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/uebersicht_depotauszuege.html']
