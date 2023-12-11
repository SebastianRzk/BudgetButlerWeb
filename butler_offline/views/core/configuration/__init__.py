from butler_offline.core.configuration_provider import CONFIGURATION_PROVIDER
from butler_offline.core.configuration_provider import ConfigurationProvider
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.viewcore import request_handler
from butler_offline.viewcore import routes
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.context.builder import generate_transactional_page_context, generate_redirect_page_context
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.state import persisted_state


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


def handle_request(request: Request, context: ConfigurationContext):
    if request.post_action_is('edit_databases'):
        dbs = request.values['dbs']
        context.configuration().set_configuration('DATABASES', dbs)
        persisted_state.DATABASES = []
        persisted_state.DATABASE_INSTANCE = None

    if request.post_action_is('add_kategorie'):
        context.einzelbuchungen().add_kategorie(request.values['neue_kategorie'])
        if 'redirect' in request.values:
            return generate_redirect_page_context('/' + str(request.values['redirect']) + '/')

    if request.post_action_is('change_themecolor'):
        context.configuration().set_configuration('THEME_COLOR', request.values['themecolor'])

    if request.post_action_is('change_colorpalette'):
        request_colors = []
        for colornumber in range(0, 20):
            if str(colornumber) + '_checked' in request.values:
                request_colors.append(request.values[str(colornumber) + '_farbe'][1:])
        context.configuration().set_configuration('DESIGN_COLORS', ','.join(request_colors))

    if request.post_action_is('set_partnername'):
        context.gemeinsame_buchungen().rename(
            context.configuration().get_configuration('PARTNERNAME'), request.values['partnername'])
        context.configuration().set_configuration('PARTNERNAME', request.values['partnername'])

    if request.post_action_is('set_ausgeschlossene_kategorien'):
        context.configuration().set_configuration('AUSGESCHLOSSENE_KATEGORIEN',
                                                  request.values['ausgeschlossene_kategorien'])
        new_set = set(list(request.values['ausgeschlossene_kategorien'].split(',')))
        context.einzelbuchungen().ausgeschlossene_kategorien = new_set

    farbmapping = []
    kategorien = sorted(list(context.einzelbuchungen().get_alle_kategorien()))
    design_colors = context.configuration().get_configuration('DESIGN_COLORS').split(',')
    for colornumber in range(0, 20):
        checked = False
        kategorie = 'keine'
        color = design_colors[colornumber % len(design_colors)]
        len_kategorien = len(kategorien)
        if colornumber < len_kategorien:
            kategorie = kategorien[colornumber % len_kategorien]
        if colornumber < len(design_colors):
            checked = True

        farbmapping.append({
            'nummer': colornumber,
            'checked': checked,
            'farbe': color,
            'kategorie': kategorie
        })

    render_context = generate_transactional_page_context('configuration')

    if routes.CORE_CONFIGURATION_PARAM_SUCCESS_MESSAGE in request.values:
        render_context.add_user_success_message(request.values[routes.CORE_CONFIGURATION_PARAM_SUCCESS_MESSAGE])

    render_context.add('palette', farbmapping)
    default_databases = ''
    for database in persisted_state.DATABASES:
        if len(default_databases) != 0:
            default_databases = default_databases + ','
        default_databases = default_databases + database
    render_context.add('default_databases', default_databases)
    render_context.add('partnername', viewcore.name_of_partner())
    render_context.add('themecolor', context.configuration().get_configuration('THEME_COLOR'))
    render_context.add('ausgeschlossene_kategorien',
                       context.configuration().get_configuration('AUSGESCHLOSSENE_KATEGORIEN'))
    render_context.add('kategorien', kategorien)
    return render_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        context_creator=lambda db: ConfigurationContext(
            conf_provider=CONFIGURATION_PROVIDER,
            einzelbuchungen=db.einzelbuchungen,
            gemeinsame_buchungen=db.gemeinsamebuchungen
        ),
        html_base_page='core/configuration.html'
    )
