from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.request_stubs import PostRequest
from butler_offline.views.sparen import add_depotwert
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler


def test_init():
    context = add_depotwert.handle_request(
        GetRequest(),
        context=add_depotwert.AddDepotwertContext(depotwerte=Depotwerte())
    )
    assert context.get('approve_title') == 'Depotwert hinzufügen'
    assert context.get('types') == Depotwerte().TYPES


def test_transaction_id_should_be_in_context():
    context = add_depotwert.handle_request(
        GetRequest(),
        context=add_depotwert.AddDepotwertContext(depotwerte=Depotwerte())
    )
    assert context.is_transactional()


def test_add_should_add_depotwert():
    depotwerte = Depotwerte()
    typ_etf = depotwerte.TYP_ETF

    add_depotwert.handle_request(
        request=PostRequest(
            {'action': 'add',
             'name': '1name',
             'isin': '1isin',
             'typ': typ_etf
             }
        ),
        context=add_depotwert.AddDepotwertContext(depotwerte=depotwerte)
    )

    assert depotwerte.select().count() == 1
    assert depotwerte.get(0) == {
        'Name': '1name',
        'ISIN': '1isin',
        'Typ': typ_etf,
        'index': 0
    }


def test_add_depotwert_should_show_in_recently_added():
    depotwerte = Depotwerte()
    typ_etf = depotwerte.TYP_ETF

    result = add_depotwert.handle_request(
        request=PostRequest(
            {'action': 'add',
             'name': '1name',
             'isin': '1isin',
             'typ': typ_etf
             }
        ),
        context=add_depotwert.AddDepotwertContext(
            depotwerte=depotwerte
        )
    )
    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'plus'
    assert result_element['Name'] == '1name'
    assert result_element['Isin'] == '1isin'
    assert result_element['Typ'] == typ_etf


def test_edit_depotwert():
    depotwerte = Depotwerte()
    typ_etf = depotwerte.TYP_ETF
    typ_fond = depotwerte.TYP_FOND

    depotwerte.add(
        name='1name',
        typ=typ_etf,
        isin='1isin'
    )

    result = add_depotwert.handle_request(
        request=PostRequest(
            {'action': 'add',
             'edit_index': 0,
             'name': '2name',
             'isin': '2isin',
             'typ': typ_fond
             }
        ),
        context=add_depotwert.AddDepotwertContext(
            depotwerte=depotwerte
        )
    )

    assert depotwerte.select().count() == 1
    assert depotwerte.get(0) == {
        'Name': '2name',
        'ISIN': '2isin',
        'Typ': typ_fond,
        'index': 0
    }

    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'pencil'
    assert result_element['Name'] == '2name'
    assert result_element['Isin'] == '2isin'
    assert result_element['Typ'] == typ_fond


def test_edit_depotwert_with_underscore_should_return_error():
    depotwerte = Depotwerte()
    typ_etf = depotwerte.TYP_ETF
    depotwerte.add(
        name='1name',
        isin='1isin',
        typ=typ_etf
    )

    result = add_depotwert.handle_request(
        request=PostRequest(
            {'action': 'add',
             'edit_index': 0,
             'name': '2name',
             'isin': '2_isin',
             'typ': typ_etf
             }
        ),
        context=add_depotwert.AddDepotwertContext(
            depotwerte=depotwerte
        )
    )
    assert result.is_error()
    assert result.error_text() == 'ISIN darf kein Unterstrich "_" enthalten.'


def test_edit_call_from_ueberischt_should_preset_values_and_rename_button():
    depotwerte = Depotwerte()
    typ_etf = depotwerte.TYP_ETF
    depotwerte.add(
        name='1name',
        isin='1isin',
        typ=typ_etf
    )

    context = add_depotwert.handle_request(
        PostRequest({'action': 'edit', 'edit_index': '0'}),
        context=add_depotwert.AddDepotwertContext(depotwerte=depotwerte)
    )
    assert context.get('approve_title') == 'Depotwert aktualisieren'
    preset = context.get('default_item')

    assert preset['edit_index'] == '0'
    assert preset['name'] == '1name'
    assert preset['isin'] == '1isin'
    assert preset['typ'] == typ_etf


def test_index_should_be_secured_by_request_handler():
    def index():
        add_depotwert.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/add_depotwert.html']
