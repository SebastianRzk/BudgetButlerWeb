import datetime

import numpy as np

from butler_offline.core import file_system, configuration_provider
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.online_services.butler_online.session import OnlineAuth
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.requester_stub import RequesterStub
from butler_offline.viewcore import requester
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.state.non_persisted_state import NonPersistedContext
from butler_offline.views.core import configuration
from butler_offline.views.shared import import_data


def test_pad_protocoll_with_no_protocoll_should_add_https():
    assert import_data.add_protokoll_if_needed('myurl') == 'https://myurl'


def test_transaction_id_should_be_in_context():
    context = import_data.handle_request(
        request=GetRequest(),
        context=get_initial_context())
    assert context.is_ok()
    assert context.is_transactional()


def test_pad_protocoll_with_existing_protocoll_should_not_change_protocoll():
    assert import_data.add_protokoll_if_needed('http://myurl') == 'http://myurl'
    assert import_data.add_protokoll_if_needed('https://myurl') == 'https://myurl'


def test_init_should_return_index_page():
    context = import_data.handle_request(
        request=GetRequest(),
        context=get_initial_context()
    )
    assert context.is_ok()
    assert not context.is_page_to_render_overwritten()
    assert context.pagename() == 'import'


_IMPORT_DATA = '''
#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-06,Essen,Edeka,-10.0,True
#######MaschinenimportEnd
'''


def test_add_passende_kategorie_should_import_value():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)
    filesystem = FileSystemStub()

    context = import_data.handle_request(
        request=PostRequest({'import': _IMPORT_DATA}),
        context=get_initial_context(einzelbuchungen=einzelbuchungen, filesystem=filesystem)
    )
    assert context.pagename() == 'import'
    assert not context.is_page_to_render_overwritten()
    assert einzelbuchungen.select().select_year(2017).sum() == -11.54
    assert filesystem.get_interaction_count() == 1


def test_import_with_one_buchung_should_show_success_single_message():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

    context = import_data.handle_request(
        request=PostRequest({'import': _IMPORT_DATA}),
        context=get_initial_context(einzelbuchungen=einzelbuchungen)
    )
    assert context.user_success_message()
    assert context.user_success_message().content() == '1 Buchung wurde importiert'


def test_import_with_one_buchung_should_show_success_message():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

    context = import_data.handle_request(
        request=PostRequest({'import': _IMPORT_DATA_GEMEINSAM}),
        context=get_initial_context(einzelbuchungen=einzelbuchungen)
    )

    assert context.user_success_message()
    assert context.user_success_message().content() == '2 Buchungen wurden importiert'


_JSON_IMPORT_DATA_GEMEINSAM = '''
[
{"id":"122","datum":"2019-01-01","name":"Testausgabe1","kategorie":"Essen","wert":"-1.3", "user": "unknown", "zielperson": "online user name"},
{"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Essen","wert":"-0.9", "user": "unknown", "zielperson": "Partner"}
]
'''


def test_gemeinsam_add_passende_kategorie_should_import_value():
    einzelbuchungen = Einzelbuchungen()
    gemeinsamebuchungen = Gemeinsamebuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

    context = import_data.handle_request_internally(
        request=PostRequest({'import': _IMPORT_DATA_GEMEINSAM}),
        gemeinsam=True,
        context=get_initial_context(einzelbuchungen=einzelbuchungen, gemeinsamebuchungen=gemeinsamebuchungen)
    )

    assert context.is_ok()
    assert context.pagename() == 'import'
    assert not context.is_page_to_render_overwritten()
    assert gemeinsamebuchungen.select().count() == 2


def test_import_should_write_into_abrechnungen():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)
    filesystem = FileSystemStub()

    import_data.handle_request(
        request=PostRequest({'import': _IMPORT_DATA}),
        context=get_initial_context(einzelbuchungen=einzelbuchungen, filesystem=filesystem)
    )

    written_abrechnung = None
    for key in filesystem.get_all_files():
        if key.startswith('./Import'):
            written_abrechnung = filesystem.read(key)

    assert list(map(lambda x: x.strip(), written_abrechnung)) == _IMPORT_DATA.split('\n')


def test_adde_unpassenden_kategorie_should_show_import_mapping_page():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'unbekannt', 'some name', -1.54)

    context = import_data.handle_request(
        request=PostRequest({'import': _IMPORT_DATA}),
        context=get_initial_context(einzelbuchungen=einzelbuchungen)
    )
    assert context.is_page_to_render_overwritten()
    assert context.page_to_render() == 'shared/import_mapping.html'
    assert context.generate_basic_page_context('asdf', 'asdf')['element_titel'] == 'Kategorien zuweisen'


def test_add_unpassenden_kategorie_mit_passendem_mapping_should_import_value():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'Unpassend', 'some name', -1.54)

    context = import_data.handle_request(
        request=PostRequest({'import': _IMPORT_DATA, 'Essen_mapping': 'als Unpassend importieren'}),
        context=get_initial_context(einzelbuchungen=einzelbuchungen)
    )
    assert context.get_page_context_map()['element_titel'] == 'Export / Import'
    assert einzelbuchungen.select().select_year(2017).sum() == -11.54


_IMPORT_DATA_GEMEINSAM = '''\n
#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Person,Dynamisch
2019-01-01,Essen,Testausgabe1,-1.3,TestUser,False
2019-07-11,Essen,Testausgabe2,-0.9,conf.partnername,False
#######MaschinenimportEnd
'''

_JSON_IMPORT_DATA = '''
[
{"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Essen","wert":"-1.3"},
{"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Essen","wert":"-0.9"}
]
'''

_JSON_DATA_PARTNER = '''
{
    "partnername": "OnlinePartner"
}
'''


def test_einzelbuchung_import_adde_passende_kategorie_should_import_value():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

    requester.INSTANCE = RequesterStub({'https://test.test/api/einzelbuchungen': _JSON_IMPORT_DATA})

    page_context = get_initial_context(einzelbuchungen=einzelbuchungen)
    context = import_data.handle_request(
        request=PostRequest({'action': 'load_online_transactions',
                             'email': '',
                             'server': 'test.test/',
                             'password': ''}),
        context=page_context
    )

    assert context.is_ok()
    assert context.is_redirect()
    assert context.redirect_target_url() == 'https://test.test/offlinelogin'

    context = page_context.non_persisted_state().butler_online_function(any_auth())

    assert context.is_ok()
    assert context.get_page_context_map()['element_titel'] == 'Export / Import'
    assert einzelbuchungen.select().count() == 3
    assert einzelbuchungen.get(1) == {'Datum': datum('11.07.2019'),
                                      'Dynamisch': False,
                                      'Kategorie': 'Essen',
                                      'Name': 'Testausgabe2',
                                      'Tags': np.nan,
                                      'Wert': -0.9,
                                      'index': 1}
    assert einzelbuchungen.get(2) == {'Datum': datum('15.07.2019'),
                                      'Dynamisch': False,
                                      'Kategorie': 'Essen',
                                      'Name': 'Testausgabe1',
                                      'Tags': np.nan,
                                      'Wert': -1.3,
                                      'index': 2}

    assert requester.instance().complete_call_count() == 2


def any_auth():
    return OnlineAuth(online_name="online user name", cookies="<--cookie-->")


def test_gemeinsam_import_adde_passende_kategorie_should_import_value():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)
    gemeinsamebuchungen = Gemeinsamebuchungen()

    requester.INSTANCE = RequesterStub({'https://test.test/api/gemeinsame_buchungen': _JSON_IMPORT_DATA_GEMEINSAM})

    page_context = get_initial_context(einzelbuchungen=einzelbuchungen, gemeinsamebuchungen=gemeinsamebuchungen,
                                       name='TestUser')
    context = import_data.handle_request(
        request=PostRequest({'action': 'load_online_gemeinsame_transactions',
                             'email': '',
                             'server': 'test.test/',
                             'password': ''}),
        context=page_context
    )

    assert context.is_redirect()
    assert context.redirect_target_url() == 'https://test.test/offlinelogin'

    context = page_context.non_persisted_state().butler_online_function(any_auth())

    assert context.get_page_context_map()['element_titel'] == 'Export / Import'
    assert gemeinsamebuchungen.select().count() == 2
    assert gemeinsamebuchungen.get(0)['Name'] == 'Testausgabe1'
    assert gemeinsamebuchungen.get(0)['Person'] == 'TestUser'
    assert gemeinsamebuchungen.get(1)['Name'] == 'Testausgabe2'

    assert requester.instance().call_count_of('https://test.test/api/gemeinsame_buchungen') == 2
    assert requester.instance().complete_call_count() == 2


_JSON_IMPORT_DATA_GEMEINSAM_WRONG_PARTNER = '''
[
{"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Essen","wert":"-1.3", "user":"TestUserFalsch","zielperson":"PartnerFalsch"},
{"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Essen","wert":"-0.9", "user":"TestUserFalsch","zielperson":"online user name"}
]
'''


def test_gemeinsam_import_with_unpassenden_partnername_should_import_value_and_replace_name():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)
    gemeinsamebuchungen = Gemeinsamebuchungen()

    requester.INSTANCE = RequesterStub(
        {'https://test.test/api/gemeinsame_buchungen': _JSON_IMPORT_DATA_GEMEINSAM_WRONG_PARTNER})

    page_context = get_initial_context(einzelbuchungen=einzelbuchungen, gemeinsamebuchungen=gemeinsamebuchungen,
                                       name='TestUser')
    context = import_data.handle_request(
        request=PostRequest({'action': 'load_online_gemeinsame_transactions',
                             'email': '',
                             'server': 'test.test',
                             'password': ''}),
        context=page_context
    )

    assert context.is_redirect()
    assert context.redirect_target_url() == 'https://test.test/offlinelogin'

    context = page_context.non_persisted_state().butler_online_function(any_auth())
    assert context.get_page_context_map()['element_titel'] == 'Export / Import'
    assert gemeinsamebuchungen.select().count() == 2
    assert gemeinsamebuchungen.get(0) == {
        'Datum': datetime.date(2019, 7, 11),
        'Dynamisch': False,
        'Kategorie': 'Essen',
        'Name': 'Testausgabe2',
        'Person': 'TestUser',
        'Wert': -0.9,
        'index': 0}

    assert gemeinsamebuchungen.get(1) == {
        'Datum': datetime.date(2019, 7, 15),
        'Dynamisch': False,
        'Kategorie': 'Essen',
        'Name': 'Testausgabe1',
        'Person': 'conf.partnername',
        'Wert': -1.3,
        'index': 1}

    assert requester.instance().call_count_of('https://test.test/api/gemeinsame_buchungen') == 2
    assert requester.instance().complete_call_count() == 2


def test_gemeinsam_import_with_unpassenden_kategorie_should_import_value_and_requestmapping():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2017'), 'KeinEssen', 'some name', -1.54)
    gemeinsamebuchungen = Gemeinsamebuchungen()

    requester.INSTANCE = RequesterStub({'https://test.test/api/gemeinsame_buchungen': _JSON_IMPORT_DATA_GEMEINSAM})

    page_context = get_initial_context(einzelbuchungen=einzelbuchungen, gemeinsamebuchungen=gemeinsamebuchungen,
                                       name='TestUser')
    context = import_data.handle_request(
        request=PostRequest({'action': 'load_online_gemeinsame_transactions',
                             'email': '',
                             'server': 'test.test',
                             'password': ''}),
        context=page_context
    )

    assert context.is_redirect()
    assert context.redirect_target_url() == 'https://test.test/offlinelogin'

    context = page_context.non_persisted_state().butler_online_function(any_auth())

    assert context.get_page_context_map()['element_titel'] == 'Kategorien zuweisen'
    assert context.get('import') == _IMPORT_DATA_GEMEINSAM
    assert context.get('unpassende_kategorien') == ['Essen']

    context = import_data.handle_request(
        request=PostRequest({'action': 'map_and_push',
                             'Essen_mapping': 'neue Kategorie anlegen',
                             'import': _IMPORT_DATA_GEMEINSAM}),
        context=get_initial_context(
            einzelbuchungen=einzelbuchungen,
            gemeinsamebuchungen=gemeinsamebuchungen,
            name='TestUser'
        )
    )

    assert context.get_page_context_map()['element_titel'] == 'Export / Import'
    assert gemeinsamebuchungen.select().count() == 2
    assert gemeinsamebuchungen.content.Person[0] == 'TestUser'
    assert gemeinsamebuchungen.content.Person[1] == 'conf.partnername'

    assert gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
    assert gemeinsamebuchungen.content.Kategorie[1] == 'Essen'

    assert requester.instance().complete_call_count() == 2


def test_set_kategorien_with_ausgeschlossene_kategoerien_should_hide_ausgeschlossene_kategorien():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('20.01.1990'), 'JaEins', 'SomeTitle', -10)
    einzelbuchungen.add(datum('20.01.1990'), 'NeinEins', 'SomeTitle', -10)
    einzelbuchungen.add(datum('20.01.1990'), 'JaZwei', 'SomeTitle', -10)
    gemeinsamebuchungen = Gemeinsamebuchungen()

    configuration.handle_request(
        request=PostRequest({'action': 'set_ausgeschlossene_kategorien', 'ausgeschlossene_kategorien': 'NeinEins'}),
        context=configuration.ConfigurationContext(
            einzelbuchungen=einzelbuchungen,
            conf_provider=configuration_provider.CONFIGURATION_PROVIDER,
            gemeinsame_buchungen=gemeinsamebuchungen
        )
    )

    requester.INSTANCE = RequesterStub({
        'https://test.test/api/kategorien': '',
        'https://test.test/api/kategorien/batch': ''})

    page_context = get_initial_context(einzelbuchungen=einzelbuchungen, gemeinsamebuchungen=gemeinsamebuchungen,
                                       name='TestUser')
    context = import_data.handle_request(
        request=PostRequest({'action': 'set_kategorien',
                             'email': '',
                             'server': 'test.test',
                             'password': ''}),
        context=page_context
    )

    assert context.is_redirect()
    assert context.redirect_target_url() == 'https://test.test/offlinelogin'

    context = page_context.non_persisted_state().butler_online_function(any_auth())

    assert context.user_success_message()
    assert context.user_success_message().content() == 'Kategorien erfolgreich in die Online-Version übertragen.'
    assert requester.instance().data_of_request('https://test.test/api/kategorien/batch')[0] == ['JaEins', 'JaZwei']
    assert requester.instance().complete_call_count() == 2


def test_upload_data():
    gemeinsamebuchungen = Gemeinsamebuchungen()

    gemeinsamebuchungen.add(datum('1.1.2020'), 'kategorie1', 'name1', 1.11, 'TestUser')
    gemeinsamebuchungen.add(datum('2.2.2020'), 'kategorie2', 'name2', 2.22, 'conf.partnername')

    requester.INSTANCE = RequesterStub({'https://test.test/api/gemeinsame_buchung/batch': '{"result": "OK"}'})

    page_context = get_initial_context(gemeinsamebuchungen=gemeinsamebuchungen, name='TestUser')
    context = import_data.handle_request(
        request=PostRequest({'action': 'upload_gemeinsame_transactions',
                             'email': '',
                             'server': 'test.test',
                             'password': ''}),
        context=page_context
    )

    assert context.is_redirect()
    assert context.redirect_target_url() == 'https://test.test/offlinelogin'

    context = page_context.non_persisted_state().butler_online_function(any_auth())

    assert gemeinsamebuchungen.select().count() == 0
    assert context.user_success_message()
    assert context.user_success_message().content() == '2 Buchungen wurden erfolgreich hochgeladen.'

    assert requester.INSTANCE.data_of_request('https://test.test/api/gemeinsame_buchung/batch') == [
        [
            {
                'datum': '2020-01-01',
                'kategorie': 'kategorie1',
                'name': 'name1',
                'eigeneBuchung': True,
                'wert': 1.11
            },
            {
                'datum': '2020-02-02',
                'kategorie': 'kategorie2',
                'name': 'name2',
                'eigeneBuchung': False,
                'wert': 2.22
            }
        ]
    ]


def test_upload_data_fehler():
    gemeinsamebuchungen = Gemeinsamebuchungen()

    gemeinsamebuchungen.add(datum('1.1.2020'), 'kategorie1', 'name1', 1.11, 'TestUser')
    gemeinsamebuchungen.add(datum('2.2.2020'), 'kategorie2', 'name2', 2.22, 'conf.partnername')

    requester.INSTANCE = RequesterStub({'https://test.test/api/gemeinsame_buchung/batch': '{"result": "error"}'})

    page_context = get_initial_context(gemeinsamebuchungen=gemeinsamebuchungen, name='TestUser')
    context = import_data.handle_request(
        request=PostRequest({'action': 'upload_gemeinsame_transactions',
                             'email': '',
                             'server': 'test.test',
                             'password': ''}),
        context=page_context
    )

    assert context.is_redirect()
    assert context.redirect_target_url() == 'https://test.test/offlinelogin'

    context = page_context.non_persisted_state().butler_online_function(any_auth())

    assert context.user_error_message()
    assert context.user_error_message().content() == 'Fehler beim Hochladen der gemeinsamen Buchungen.'
    assert gemeinsamebuchungen.select().count() == 2
    assert requester.INSTANCE.data_of_request('https://test.test/api/gemeinsame_buchung/batch') == [
        [
            {
                'datum': '2020-01-01',
                'kategorie': 'kategorie1',
                'name': 'name1',
                'eigeneBuchung': True,
                'wert': 1.11
            },
            {
                'datum': '2020-02-02',
                'kategorie': 'kategorie2',
                'name': 'name2',
                'eigeneBuchung': False,
                'wert': 2.22
            }
        ]
    ]


def get_initial_context(
        name: str = 'asdf',
        einzelbuchungen: Einzelbuchungen = Einzelbuchungen(),
        gemeinsamebuchungen: Gemeinsamebuchungen = Gemeinsamebuchungen(),
        filesystem: file_system.FileSystemImpl = FileSystemStub(),
        conf: configuration_provider.ConfigurationProvider = configuration_provider.DictConfiguration({
            'ONLINE_DEFAULT_SERVER': 'online.default.server',
            'ONLINE_DEFAULT_USER': 'online.default.user',
            'PARTNERNAME': 'conf.partnername'
        })
) -> import_data.ImportDataContext:
    return import_data.ImportDataContext(
        name=name,
        einzelbuchungen=einzelbuchungen,
        gemeinsamebuchungen=gemeinsamebuchungen,
        filesystem=filesystem,
        conf=conf,
        non_persisted_state=NonPersistedContext()
    )
