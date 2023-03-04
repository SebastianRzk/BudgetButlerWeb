from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context import generate_transactional_context, generate_redirect_context
from butler_offline.core.configuration_provider import ConfigurationProvider
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.core.configuration_provider import CONFIGURATION_PROVIDER


class ConfigurationContext:
    def __init__(self,
                 conf_provider: ConfigurationProvider,
                 einzelbuchungen: Einzelbuchungen,
                 gemeinsame_buchungen: Gemeinsamebuchungen):
        self._configuration_provider = conf_provider
        self._einzelbuchungen = einzelbuchungen
        self._gemeinsame_buchungen = gemeinsame_buchungen

    def configuration(self) -> ConfigurationProvider:
        return self._configuration_provider

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen

    def gemeinsame_buchungen(self) -> Gemeinsamebuchungen:
        return self._gemeinsame_buchungen


def _handle_request(request, context: ConfigurationContext):
    if post_action_is(request, 'edit_databases'):
        dbs = request.values['dbs']
        context.configuration().set_configuration('DATABASES', dbs)
        persisted_state.DATABASES = []
        persisted_state.DATABASE_INSTANCE = None

    if post_action_is(request, 'add_kategorie'):
        context.einzelbuchungen().add_kategorie(request.values['neue_kategorie'])
        if 'redirect' in request.values:
            return generate_redirect_context('/' + str(request.values['redirect']) + '/')

    if post_action_is(request, 'change_themecolor'):
        context.configuration().set_configuration('THEME_COLOR', request.values['themecolor'])

    if post_action_is(request, 'change_colorpalette'):
        request_colors = []
        for colornumber in range(0, 20):
            if str(colornumber) + '_checked' in request.values:
                request_colors.append(request.values[str(colornumber) + '_farbe'][1:])
        context.configuration().set_configuration('DESIGN_COLORS', ','.join(request_colors))

    if post_action_is(request, 'set_partnername'):
        context.gemeinsame_buchungen().rename(viewcore.name_of_partner(), request.values['partnername'])
        context.configuration().set_configuration('PARTNERNAME', request.values['partnername'])

    if post_action_is(request, 'set_ausgeschlossene_kategorien'):
        context.configuration().set_configuration('AUSGESCHLOSSENE_KATEGORIEN', request.values['ausgeschlossene_kategorien'])
        new_set = set(list(request.values['ausgeschlossene_kategorien'].split(',')))
        context.einzelbuchungen().ausgeschlossene_kategorien = new_set

    farbmapping = []
    kategorien = sorted(list(context.einzelbuchungen().get_alle_kategorien()))
    for colornumber in range(0, 20):
        checked = False
        kategorie = 'keine'
        color = viewcore.design_colors()[colornumber % len(viewcore.design_colors())]
        len_kategorien = len(kategorien)
        if colornumber < len_kategorien:
            kategorie = kategorien[colornumber % len_kategorien]
        if colornumber < len(viewcore.design_colors()):
            checked = True

        farbmapping.append({
            'nummer': colornumber,
            'checked': checked,
            'farbe': color,
            'kategorie': kategorie
            })

    render_context = generate_transactional_context('configuration')
    render_context['palette'] = farbmapping
    default_databases = ''
    for db in persisted_state.DATABASES:
        if len(default_databases) != 0:
            default_databases = default_databases + ','
        default_databases = default_databases + db
    render_context['default_databases'] = default_databases
    render_context['partnername'] = viewcore.name_of_partner()
    render_context['themecolor'] = context.configuration().get_configuration('THEME_COLOR')
    render_context['ausgeschlossene_kategorien'] = context.configuration().get_configuration('AUSGESCHLOSSENE_KATEGORIEN')
    return render_context


def index(request):
    def handle_request_migration(r):
        return _handle_request(r, ConfigurationContext(
            conf_provider=CONFIGURATION_PROVIDER,
            einzelbuchungen=persisted_state.database_instance().einzelbuchungen,
            gemeinsame_buchungen=persisted_state.database_instance().gemeinsamebuchungen
        ))
    return request_handler.handle_request(request, handle_request_migration, 'core/configuration.html')


