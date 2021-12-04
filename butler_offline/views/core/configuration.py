from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import request_handler
from butler_offline.core import configuration_provider


def _handle_request(request):
    if post_action_is(request, 'edit_databases'):
        dbs = request.values['dbs']
        configuration_provider.set_configuration('DATABASES', dbs)
        persisted_state.DATABASES = []
        persisted_state.DATABASE_INSTANCE = None

    if post_action_is(request, 'add_kategorie'):
        persisted_state.database_instance().einzelbuchungen.add_kategorie(request.values['neue_kategorie'])

    if post_action_is(request, 'change_themecolor'):
        configuration_provider.set_configuration('THEME_COLOR', request.values['themecolor'])

    if post_action_is(request, 'change_colorpalette'):
        request_colors = []
        for colornumber in range(0, 20):
            if str(colornumber) + '_checked' in request.values:
                request_colors.append(request.values[str(colornumber) + '_farbe'][1:])
        configuration_provider.set_configuration('DESIGN_COLORS', ','.join(request_colors))

    if post_action_is(request, 'set_partnername'):
        persisted_state.database_instance().gemeinsamebuchungen.rename(viewcore.name_of_partner(), request.values['partnername'])
        configuration_provider.set_configuration('PARTNERNAME', request.values['partnername'])

    if post_action_is(request, 'set_ausgeschlossene_kategorien'):
        configuration_provider.set_configuration('AUSGESCHLOSSENE_KATEGORIEN', request.values['ausgeschlossene_kategorien'])
        new_set = set(list(request.values['ausgeschlossene_kategorien'].split(',')))
        persisted_state.database_instance().einzelbuchungen.ausgeschlossene_kategorien = new_set

    farbmapping = []
    kategorien = sorted(list(persisted_state.database_instance().einzelbuchungen.get_alle_kategorien()))
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

    context = viewcore.generate_transactional_context('configuration')
    context['palette'] = farbmapping
    default_databases = ''
    for db in persisted_state.DATABASES:
        if len(default_databases) != 0:
            default_databases = default_databases + ','
        default_databases = default_databases + db
    context['default_databases'] = default_databases
    context['partnername'] = viewcore.name_of_partner()
    context['themecolor'] = configuration_provider.get_configuration('THEME_COLOR')
    context['ausgeschlossene_kategorien'] = configuration_provider.get_configuration('AUSGESCHLOSSENE_KATEGORIEN')
    return context

def index(request):
    return request_handler.handle_request(request, _handle_request, 'core/configuration.html')

