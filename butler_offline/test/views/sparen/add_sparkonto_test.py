from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.request_stubs import PostRequest
from butler_offline.views.sparen import add_sparkoto
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler


def basic_test_context(kontos: Kontos = Kontos()) -> add_sparkoto.AddSparkontoContext:
    return add_sparkoto.AddSparkontoContext(
        kontos=kontos
    )


def test_init():
    context = add_sparkoto.handle_request(
        request=GetRequest(),
        context=basic_test_context()
    )
    assert context.is_ok()
    assert context.get('approve_title') == 'Sparkonto hinzufügen'


def test_transaction_id_should_be_in_context():
    context = add_sparkoto.handle_request(
        request=GetRequest(),
        context=basic_test_context()
    )
    assert context.is_transactional()


def test_add_should_add_sparkonto():
    kontos = Kontos()
    add_sparkoto.handle_request(
        request=PostRequest(
            {'action': 'add',
             'kontotyp': '1typ',
             'kontoname': '1name'
             }
        ),
        context=basic_test_context(kontos=kontos)
    )

    assert kontos.select().count() == 1
    assert kontos.get(0) == {'Kontoname': '1name', 'Kontotyp': '1typ', 'index': 0}


def test_add_with_underscore_in_name_should_return_error():
    result = add_sparkoto.handle_request(
        request=PostRequest(
            {'action': 'add',
             'kontotyp': '1typ',
             'kontoname': '1_name'
             }
        ),
        context=basic_test_context()
    )

    assert result.is_error()
    assert result.error_text() == 'Kontoname darf kein Unterstrich "_" enthalten.'


def test_add_sparkonto_should_show_in_recently_added():
    result = add_sparkoto.handle_request(
        request=PostRequest(
            {'action': 'add',
             'kontotyp': '1typ',
             'kontoname': '1name'
             }
        ),
        context=basic_test_context())

    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'plus'
    assert result_element['Kontotyp'] == '1typ'
    assert result_element['Kontoname'] == '1name'


def test_edit_sparkonto():
    kontos = Kontos()
    add_sparkoto.handle_request(
        request=PostRequest(
            {'action': 'add',
             'kontotyp': '1typ',
             'kontoname': '1name'
             }
        ),
        context=basic_test_context(kontos=kontos)
    )

    result = add_sparkoto.handle_request(
        request=PostRequest(
            {'action': 'add',
             'edit_index': 0,
             'kontotyp': '2typ',
             'kontoname': '2name'
             }
        ),
        context=basic_test_context(kontos=kontos)
    )

    assert kontos.select().count() == 1
    assert kontos.get(0) == {'Kontoname': '2name', 'Kontotyp': '2typ', 'index': 0}

    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'pencil'
    assert result_element['Kontotyp'] == '2typ'
    assert result_element['Kontoname'] == '2name'


def test_edit_call_from_ueberischt_should_preset_values_and_rename_button():
    kontos = Kontos()
    add_sparkoto.handle_request(
        request=PostRequest(
            {'action': 'add',
             'kontotyp': '1typ',
             'kontoname': '1name'
             }
        ),
        context=basic_test_context(kontos=kontos))

    context = add_sparkoto.handle_request(
        request=PostRequest({'action': 'edit', 'edit_index': '0'}),
        context=basic_test_context(kontos=kontos)
    )
    assert context.get('approve_title') == 'Sparkonto aktualisieren'
    preset = context.get('default_item')

    assert preset['edit_index'] == '0'
    assert preset['kontotyp'] == '1typ'
    assert preset['kontoname'] == '1name'


def test_index_should_be_secured_by_request_handler():
    def index():
        add_sparkoto.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/add_sparkonto.html']
