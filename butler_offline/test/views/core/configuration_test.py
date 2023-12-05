from butler_offline.core.configuration_provider import DictConfiguration
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.request_stubs import PostRequest
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.routes import CORE_CONFIGURATION_PARAM_SUCCESS_MESSAGE
from butler_offline.views.core import configuration


def generate_basic_test_context(
        einzelbuchungen: Einzelbuchungen = Einzelbuchungen(),
        gemeinsamebuchungen: Gemeinsamebuchungen = Gemeinsamebuchungen()
):
    conf: DictConfiguration = DictConfiguration(
        {
            'THEME_COLOR': 'conf.theme.color',
            'AUSGESCHLOSSENE_KATEGORIEN': ['conf.ausgeschlossenene.kategorie'],
            'PARTNERNAME': 'conf.partnername',
            'DESIGN_COLORS': 'conf.color1,conf.color2'
        }
    )
    return configuration.ConfigurationContext(
        conf_provider=conf,
        einzelbuchungen=einzelbuchungen,
        gemeinsame_buchungen=gemeinsamebuchungen
    )


def test_init():
    result = configuration.handle_request(
        request=GetRequest(),
        context=generate_basic_test_context()
    )
    assert result.is_ok()


def test_transaction_id_should_be_in_context():
    context = configuration.handle_request(
        request=GetRequest(),
        context=generate_basic_test_context()
    )
    assert context.is_transactional()


def test_add_kategorie():
    einzelbuchungen = Einzelbuchungen()
    context = generate_basic_test_context(einzelbuchungen=einzelbuchungen)
    configuration.handle_request(
        request=PostRequest({'action': 'add_kategorie', 'neue_kategorie': 'test'}),
        context=context
    )
    assert einzelbuchungen.get_alle_kategorien() == {'test'}


def test_should_provide_kategorien_for_rename():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum=datum('01.01.2012'), kategorie='Kategorie A', name='', wert=1)
    einzelbuchungen.add(datum=datum('01.01.2012'), kategorie='Kategorie B', name='', wert=1)
    context = generate_basic_test_context(einzelbuchungen=einzelbuchungen)

    result = configuration.handle_request(
        request=GetRequest(),
        context=context
    )

    assert result.get('kategorien') == ['Kategorie A', 'Kategorie B']

def test_with_no_message_in_params_should_not_show_message():
    result = configuration.handle_request(
        request=GetRequest(),
        context=generate_basic_test_context()
    )
    assert not result.user_success_message()
    assert not result.user_error_message()


def test_with_message_in_params_should_show_message():
    result = configuration.handle_request(
        request=PostRequest(
            {
                CORE_CONFIGURATION_PARAM_SUCCESS_MESSAGE: 'my message'
            }
        ),
        context=generate_basic_test_context()
    )
    assert result.user_success_message()
    assert result.user_success_message().content() == 'my message'


def test_add_kategorie_with_redirect():
    result = configuration.handle_request(
        request=PostRequest({'action': 'add_kategorie', 'neue_kategorie': 'test', 'redirect': 'destination'}),
        context=generate_basic_test_context(einzelbuchungen=Einzelbuchungen())
    )
    assert result.is_redirect()
    assert result.redirect_target_url() == '/destination/'


def test_change_db_should_trigger_db_reload():
    context = generate_basic_test_context()
    configuration.handle_request(
        request=PostRequest({'action': 'edit_databases', 'dbs': 'test123'}),
        context=context
    )
    assert context.configuration().get_configuration('DATABASES') == 'test123'


def test_change_partnername_should_change_partnername():
    context = generate_basic_test_context()
    assert context.configuration().get_configuration('PARTNERNAME') == 'conf.partnername'
    configuration.handle_request(
        request=PostRequest({'action': 'set_partnername', 'partnername': 'testpartner'}),
        context=context
    )
    assert context.configuration().get_configuration('PARTNERNAME') == 'testpartner'


def test_change_themecolor_should_change_themecolor():
    context = generate_basic_test_context()
    assert context.configuration().get_configuration('THEME_COLOR') == 'conf.theme.color'
    configuration.handle_request(
        request=PostRequest({'action': 'change_themecolor', 'themecolor': '#000000'}),
        context=context
    )
    assert context.configuration().get_configuration('THEME_COLOR') == '#000000'


def test_change_schliesse_kateorien_aus_should_change_add_ausgeschlossene_kategorien():
    context = generate_basic_test_context()
    assert context.configuration().get_configuration('AUSGESCHLOSSENE_KATEGORIEN') == [
        'conf.ausgeschlossenene.kategorie']
    configuration.handle_request(
        request=PostRequest({'action': 'set_ausgeschlossene_kategorien', 'ausgeschlossene_kategorien': 'Alkohol'}),
        context=context
    )
    assert context.configuration().get_configuration('AUSGESCHLOSSENE_KATEGORIEN') == 'Alkohol'


def test_change_partnername_should_mirgrate_old_partnernames():
    name_of_partner = generate_basic_test_context().configuration().get_configuration('PARTNERNAME')
    gemeinsame_buchungen = Gemeinsamebuchungen()
    gemeinsame_buchungen.add(datum('01.01.2017'), 'kat', 'name', 1, name_of_partner)
    context = generate_basic_test_context(gemeinsamebuchungen=gemeinsame_buchungen)

    configuration.handle_request(
        request=PostRequest({'action': 'set_partnername', 'partnername': 'testpartner_renamed'}),
        context=context
    )

    database_partners = context.gemeinsame_buchungen().content.Person

    assert set(database_partners) == {'testpartner_renamed'}


def test_change_colors():
    context = generate_basic_test_context()

    assert context.configuration().get_configuration('DESIGN_COLORS') == 'conf.color1,conf.color2'
    configuration.handle_request(
        request=PostRequest({'action': 'change_colorpalette',
                             '0_checked': 'on',
                             '0_farbe': '#000000',
                             '1_checked': 'on',
                             '1_farbe': '#FFFFFF',
                             '2_farbe': '#555555'}),
        context=context
    )
    assert context.configuration().get_configuration('DESIGN_COLORS') == '000000,FFFFFF'


def test_get_colors():
    result = configuration.handle_request(
        request=GetRequest(),
        context=generate_basic_test_context()
    )
    assert result.get('palette') == [{'checked': True, 'farbe': 'conf.color1', 'kategorie': 'keine', 'nummer': 0},
                                     {'checked': True, 'farbe': 'conf.color2', 'kategorie': 'keine', 'nummer': 1},
                                     {'checked': False, 'farbe': 'conf.color1', 'kategorie': 'keine', 'nummer': 2},
                                     {'checked': False, 'farbe': 'conf.color2', 'kategorie': 'keine', 'nummer': 3},
                                     {'checked': False, 'farbe': 'conf.color1', 'kategorie': 'keine', 'nummer': 4},
                                     {'checked': False, 'farbe': 'conf.color2', 'kategorie': 'keine', 'nummer': 5},
                                     {'checked': False, 'farbe': 'conf.color1', 'kategorie': 'keine', 'nummer': 6},
                                     {'checked': False, 'farbe': 'conf.color2', 'kategorie': 'keine', 'nummer': 7},
                                     {'checked': False, 'farbe': 'conf.color1', 'kategorie': 'keine', 'nummer': 8},
                                     {'checked': False, 'farbe': 'conf.color2', 'kategorie': 'keine', 'nummer': 9},
                                     {'checked': False, 'farbe': 'conf.color1', 'kategorie': 'keine', 'nummer': 10},
                                     {'checked': False, 'farbe': 'conf.color2', 'kategorie': 'keine', 'nummer': 11},
                                     {'checked': False, 'farbe': 'conf.color1', 'kategorie': 'keine', 'nummer': 12},
                                     {'checked': False, 'farbe': 'conf.color2', 'kategorie': 'keine', 'nummer': 13},
                                     {'checked': False, 'farbe': 'conf.color1', 'kategorie': 'keine', 'nummer': 14},
                                     {'checked': False, 'farbe': 'conf.color2', 'kategorie': 'keine', 'nummer': 15},
                                     {'checked': False, 'farbe': 'conf.color1', 'kategorie': 'keine', 'nummer': 16},
                                     {'checked': False, 'farbe': 'conf.color2', 'kategorie': 'keine', 'nummer': 17},
                                     {'checked': False, 'farbe': 'conf.color1', 'kategorie': 'keine', 'nummer': 18},
                                     {'checked': False, 'farbe': 'conf.color2', 'kategorie': 'keine', 'nummer': 19}]
