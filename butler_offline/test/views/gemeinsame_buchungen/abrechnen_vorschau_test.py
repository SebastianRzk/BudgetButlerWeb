from butler_offline.test.RequestStubs import GetRequest, PostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.views.gemeinsame_buchungen import abrechnen_vorschau
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler


def test_init():
    abrechnen_vorschau.handle_request(request=GetRequest(),
                                      context=abrechnen_vorschau.AbrechnenVorschauContext(
                                          name='abc',
                                          gemeinsamebuchungen=Gemeinsamebuchungen(),
                                          einzelbuchungen=Einzelbuchungen()
                                      ))


def test__short_result__with_equal_value__should_return_equal_sentence():
    database_name = "my-name"
    name_partner = viewcore.name_of_partner()
    gemeinsame_buchungen = Gemeinsamebuchungen()

    gemeinsame_buchungen.add(datum('01.01.2010'), some_name(), some_kategorie(), -11, database_name)
    gemeinsame_buchungen.add(datum('01.01.2010'), some_name(), some_kategorie(), -11, name_partner)

    result = abrechnen_vorschau.handle_request(
        request=GetRequest(),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name=database_name,
            einzelbuchungen=Einzelbuchungen(),
            gemeinsamebuchungen=gemeinsame_buchungen
        )
    )

    assert result.is_ok()
    assert result.get('ergebnis') == 'Die gemeinsamen Ausgaben sind ausgeglichen.'


def test__short_result__with_selected_date__should_filter_entries():
    name_partner = viewcore.name_of_partner()
    self_name = 'Test_User'
    gemeinsame_buchungen = Gemeinsamebuchungen()

    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -1000, self_name)
    gemeinsame_buchungen.add(datum('15.01.2011'), some_name(), some_kategorie(), -20, name_partner)
    gemeinsame_buchungen.add(datum('15.01.2012'), some_name(), some_kategorie(), -1000, name_partner)

    result = abrechnen_vorschau.handle_request(
        request=PostRequest({'set_mindate': '2011-01-01', 'set_maxdate': '2011-02-01'}),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name=self_name,
            gemeinsamebuchungen=gemeinsame_buchungen,
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert result.is_ok()
    assert result.get('ergebnis') == 'Partner bekommt von Test_User noch 10.00€.'
    assert result.get('count') == 3
    assert result.get('set_count') == 1


def test_result__with_selektiertem_verhaeltnis():
    name_partner = viewcore.name_of_partner()
    self_name = 'Test_User'
    gemeinsame_buchungen = Gemeinsamebuchungen()

    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -50, self_name)
    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -50, name_partner)

    result = abrechnen_vorschau.handle_request(
        request=PostRequest({'set_verhaeltnis': 60}),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name=self_name,
            gemeinsamebuchungen=gemeinsame_buchungen,
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert result.is_ok()
    assert result.get(
        'ergebnis') == 'Test_User übernimmt einen Anteil von 60% der Ausgaben.' \
                       '<br>Partner bekommt von Test_User noch 10.00€.'
    assert result.get('self_soll') == '60.00'
    assert result.get('partner_soll') == '40.00'
    assert result.get('self_diff') == '-10.00'
    assert result.get('partner_diff') == '10.00'


def test_result_with_limit_partner_and_value_under_limit__should_return_default_verhaeltnis():
    name_partner = viewcore.name_of_partner()
    self_name = 'Test_User'
    gemeinsame_buchungen = Gemeinsamebuchungen()

    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -50, self_name)
    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -50, name_partner)

    result = abrechnen_vorschau.handle_request(
        request=PostRequest({'set_verhaeltnis': 50,
                             'set_limit': 'on',
                             'set_limit_fuer': name_partner,
                             'set_limit_value': 100}),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name=self_name,
            gemeinsamebuchungen=gemeinsame_buchungen,
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert result.is_ok()
    assert result.get('ergebnis') == 'Die gemeinsamen Ausgaben sind ausgeglichen.'
    assert result.get('self_soll') == '50.00'
    assert result.get('partner_soll') == '50.00'
    assert result.get('self_diff') == '0.00'
    assert result.get('partner_diff') == '0.00'


def test_result_with_limit_partner_and_value_over_limit__should_modify_verhaeltnis():
    name_partner = viewcore.name_of_partner()
    self_name = 'Test_User'
    gemeinsame_buchungen = Gemeinsamebuchungen()

    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -50, self_name)
    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -50, name_partner)

    result = abrechnen_vorschau.handle_request(
        request=PostRequest({'set_verhaeltnis': 50,
                             'set_limit': 'on',
                             'set_limit_fuer': name_partner,
                             'set_limit_value': 40}),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name=self_name,
            gemeinsamebuchungen=gemeinsame_buchungen,
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert result.is_ok()
    assert result.get(
        'ergebnis') == 'Durch das Limit bei Partner von 40 EUR wurde das Verhältnis von 50 auf 60.0 ' \
                       'aktualisiert<br>Partner bekommt von Test_User noch 10.00€.'
    assert result.get('self_soll') == '60.00'
    assert result.get('partner_soll') == '40.00'
    assert result.get('self_diff') == '-10.00'
    assert result.get('partner_diff') == '10.00'
    assert result.get('set_verhaeltnis') == 50
    assert result.get('set_verhaeltnis_real') == 60


def test_result_with_limit_self_and_value_under_limit__should_return_default_verhaeltnis():
    name_partner = viewcore.name_of_partner()
    self_name = 'Test_User'
    gemeinsame_buchungen = Gemeinsamebuchungen()

    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -50, self_name)
    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -50, name_partner)

    result = abrechnen_vorschau.handle_request(
        request=PostRequest({'set_verhaeltnis': 50,
                             'set_limit': 'on',
                             'set_limit_fuer': self_name,
                             'set_limit_value': 100}),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name=self_name,
            gemeinsamebuchungen=gemeinsame_buchungen,
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert result.is_ok()
    assert result.get('ergebnis') == 'Die gemeinsamen Ausgaben sind ausgeglichen.'
    assert result.get('self_soll') == '50.00'
    assert result.get('partner_soll') == '50.00'
    assert result.get('self_diff') == '0.00'
    assert result.get('partner_diff') == '0.00'


def test_result__with_limit_self_and_value_over_limit__should_modify_verhaeltnis():
    name_partner = viewcore.name_of_partner()
    self_name = 'Test_User'
    gemeinsame_buchungen = persisted_state.database_instance().gemeinsamebuchungen

    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -50, self_name)
    gemeinsame_buchungen.add(some_datum(), some_name(), some_kategorie(), -50, name_partner)

    untaint_database(database=persisted_state.database_instance())

    result = abrechnen_vorschau.handle_request(
        request=PostRequest({'set_verhaeltnis': 50,
                             'set_limit': 'on',
                             'set_limit_fuer': self_name,
                             'set_limit_value': 40}),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name=self_name,
            einzelbuchungen=Einzelbuchungen(),
            gemeinsamebuchungen=gemeinsame_buchungen
        )
    )

    assert result.is_ok()
    assert result.get(
               'ergebnis') == 'Durch das Limit bei Test_User von 40 EUR wurde das Verhältnis von 50 auf 40.0 ' \
                              'aktualisiert<br>Test_User bekommt von Partner noch 10.00€.'
    assert result.get('self_soll') == '40.00'
    assert result.get('partner_soll') == '60.00'
    assert result.get('self_diff') == '10.00'
    assert result.get('partner_diff') == '-10.00'


def some_name():
    return 'Some Cat.'


def some_datum():
    return datum('15.01.2010')


def test_with_empty_databse_should_return_error():
    result = abrechnen_vorschau.handle_request(
        request=GetRequest(),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name='asdf',
            gemeinsamebuchungen=Gemeinsamebuchungen(),
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert not result.is_ok()
    assert result.is_error()


def test__short_result__with_partner_more_spendings_should_return_equal_sentence():
    gemeinsame_buchungen = Gemeinsamebuchungen()
    name_partner = viewcore.name_of_partner()
    gemeinsame_buchungen.add(datum('01.01.2010'), some_name(), some_kategorie(), -11, name_partner)

    result = abrechnen_vorschau.handle_request(
        request=GetRequest(),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name='Test_User',
            gemeinsamebuchungen=gemeinsame_buchungen,
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert result.is_ok()
    assert result.get('ergebnis') == 'Partner bekommt von Test_User noch 5.50€.'


def some_kategorie():
    return ''


def test__short_result__with_self_more_spendings__should_return_equal_sentence():
    gemeinsame_buchungen = Gemeinsamebuchungen()
    name_self = 'Test_User'
    gemeinsame_buchungen.add(datum('01.01.2010'), some_name(), some_kategorie(), -11, name_self)

    result = abrechnen_vorschau.handle_request(
        request=GetRequest(),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name=name_self,
            gemeinsamebuchungen=gemeinsame_buchungen,
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert result.is_ok()
    assert result.get('ergebnis') == 'Test_User bekommt von Partner noch 5.50€.'


def test_context_should_be_transactional():
    gemeinsame_buchungen = Gemeinsamebuchungen()
    name_self = 'Test_User'
    gemeinsame_buchungen.add(datum('01.01.2010'), some_name(), some_kategorie(), -11, name_self)

    result = abrechnen_vorschau.handle_request(
        request=GetRequest(),
        context=abrechnen_vorschau.AbrechnenVorschauContext(
            name=name_self,
            gemeinsamebuchungen=gemeinsame_buchungen,
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert result.is_transactional()


def test_index_should_be_secured_by_request_handler():
    def index():
        abrechnen_vorschau.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['gemeinsame_buchungen/gemeinsamabrechnen.html']

