from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.views.sparen import uebersicht_depotwerte
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.sparen.order import Order
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.test.test import assert_info_message_keine_depotwerte_erfasst_in_context, assert_keine_message_set


def generate_basic_test_context(
        order: Order = Order(),
        depotwerte: Depotwerte = Depotwerte(),
        depotauszuege: Depotauszuege = Depotauszuege()
):
    return uebersicht_depotwerte.UebersichtDepotwerteContext(
        order=order,
        depotwerte=depotwerte,
        depotauszuege=depotauszuege,
    )


def generate_test_context_with_data():
    depotwerte = Depotwerte()
    depotwerte.add(name='depotwert1', isin='isin1', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='depotwert2', isin='isin2', typ=depotwerte.TYP_ETF)
    order = Order()
    order.add(datum('12.12.2019'), 'demoname', 'demokonto', 'isin1', 100)

    depotauszuege = Depotauszuege()
    depotauszuege.add(datum('01.01.2020'), 'isin1', 'demokonto', 90)

    return generate_basic_test_context(
        order=order,
        depotauszuege=depotauszuege,
        depotwerte=depotwerte
    )


def test_transaction_id_should_be_in_context():
    context = uebersicht_depotwerte.handle_request(
        request=GetRequest(),
        context=generate_basic_test_context()
    )
    assert context.is_ok()
    assert context.is_transactional()


def test_should_list_depotwerte():

    result = uebersicht_depotwerte.handle_request(
        request=GetRequest(),
        context=generate_test_context_with_data()
    )

    assert result.is_ok()
    assert result.get('depotwerte') == [
        {
            'index': 0,
            'name': 'depotwert1',
            'isin': 'isin1',
            'typ': 'ETF',
            'buchung': Betrag(100),
            'difference': Betrag(-10),
            'difference_is_negativ': True,
            'wert': Betrag(90)},
        {
            'index': 1,
            'name': 'depotwert2',
            'isin': 'isin2',
            'typ': 'ETF',
            'buchung': Betrag(0),
            'difference': Betrag(0),
            'difference_is_negativ': False,
            'wert': Betrag(0)}
    ]

    assert result.get('gesamt') == {
        'buchung': Betrag(100),
        'difference': Betrag(-10),
        'difference_is_negativ': True,
        'wert': Betrag(90)
    }


def test_delete():
    context = generate_test_context_with_data()
    uebersicht_depotwerte.handle_request(
        request=PostRequest({'action': 'delete', 'delete_index': '1'}),
        context=context
    )
    depotwerte = context.depotwerte()
    assert depotwerte.select().count() == 1
    assert depotwerte.get(0) == {'Name': 'depotwert1',
                                 'ISIN': 'isin1',
                                 'Typ': depotwerte.TYP_ETF,
                                 'index': 0}


def test_index_should_be_secured_by_request_handler():
    def index():
        uebersicht_depotwerte.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/uebersicht_depotwerte.html']


def test_index_with_empty_database_should_add_info_message():
    context = uebersicht_depotwerte.handle_request(
        request=GetRequest(),
        context=generate_basic_test_context()
    )
    assert_info_message_keine_depotwerte_erfasst_in_context(result=context)


def test_index_with_filled_database_should_have_no_info_message():
    context = uebersicht_depotwerte.handle_request(
        request=GetRequest(),
        context=generate_test_context_with_data()
    )
    assert_keine_message_set(result=context)
