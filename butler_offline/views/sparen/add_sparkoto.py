from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.context import generate_transactional_context, generate_error_context


def handle_request(request):
    if post_action_is(request, 'add'):
        kontoname = request.values['kontoname']
        if '_' in kontoname:
            return generate_error_context('add_depotwert', 'Kontoname darf kein Unterstrich "_" enthalten.')
        kontotyp = request.values['kontotyp']

        if "edit_index" in request.values:
            database_instance().sparkontos.edit(int(request.values['edit_index']),
                kontoname=kontoname,
                kontotyp=kontotyp)
            non_persisted_state.add_changed_sparkontos(
                {
                    'fa': 'pencil',
                    'Kontoname': kontoname,
                    'Kontotyp': kontotyp
                })

        else:
            database_instance().sparkontos.add(
                kontoname=kontoname,
                kontotyp=kontotyp)
            non_persisted_state.add_changed_sparkontos(
                {
                    'fa': 'plus',
                    'Kontoname': kontoname,
                    'Kontotyp': kontotyp
                    })

    context = generate_transactional_context('add_sparkonto')
    context['approve_title'] = 'Sparkonto hinzufügen'
    if post_action_is(request, 'edit'):
        print("Please edit:", request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        db_row = database_instance().sparkontos.get(db_index)

        default_item = {
            'edit_index': str(db_index),
            'kontotyp': db_row['Kontotyp'],
            'kontoname': db_row['Kontoname']
        }

        context['default_item'] = default_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['approve_title'] = 'Sparkonto aktualisieren'

    if 'default_item' not in context:
        context['default_item'] = {
            'kontoname': '',
            'kontotyp': ''
        }

    context['kontotypen'] = database_instance().sparkontos.KONTO_TYPEN
    context['letzte_erfassung'] = reversed(non_persisted_state.get_changed_sparkontos())
    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'sparen/add_sparkonto.html')

