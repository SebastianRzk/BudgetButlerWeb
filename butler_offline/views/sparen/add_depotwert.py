from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import non_persisted_state


def handle_request(request):
    if post_action_is(request, 'add'):
        if "edit_index" in request.values:
            database_instance().depotwerte.edit(int(request.values['edit_index']),
                name=request.values['name'],
                isin=request.values['isin'])
            non_persisted_state.add_changed_depotwerte(
                {
                    'fa': 'pencil',
                    'Name': request.values['name'],
                    'Isin': request.values['isin']
                })
        else:
            database_instance().depotwerte.add(
                name=request.values['name'],
                isin=request.values['isin'])
            non_persisted_state.add_changed_depotwerte(
                {
                    'fa': 'plus',
                    'Name': request.values['name'],
                    'Isin': request.values['isin']
                    })

    context = viewcore.generate_transactional_context('add_depotwert')
    context['approve_title'] = 'Depotwert hinzufügen'

    if post_action_is(request, 'edit'):
        db_index = int(request.values['edit_index'])
        db_row = database_instance().depotwerte.get(db_index)

        default_item = {
            'edit_index': str(db_index),
            'name': db_row['Name'],
            'isin': db_row['ISIN']
        }

        context['default_item'] = default_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['approve_title'] = 'Depotwert aktualisieren'

    if 'default_item' not in context:
        context['default_item'] = {
            'name': '',
            'isin': ''
        }

    context['letzte_erfassung'] = reversed(non_persisted_state.get_changed_depotwerte())
    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'sparen/add_depotwert.html')

