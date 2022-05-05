from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import non_persisted_state


def handle_request(request):
    if post_action_is(request, 'add'):
        isin = request.values['isin']
        if '_' in isin:
            return viewcore.generate_error_context('add_depotwert', 'ISIN darf kein Unterstrich "_" enthalten.')
        name = request.values['name']
        typ = request.values['typ']

        if "edit_index" in request.values:
            database_instance().depotwerte.edit(int(request.values['edit_index']),
                name=name,
                isin=isin,
                typ=typ)
            non_persisted_state.add_changed_depotwerte(
                {
                    'fa': 'pencil',
                    'Name': name,
                    'Isin': isin,
                    'Typ': typ
                })
        else:
            database_instance().depotwerte.add(
                name=name,
                isin=isin,
                typ=typ)
            non_persisted_state.add_changed_depotwerte(
                {
                    'fa': 'plus',
                    'Name': name,
                    'Isin': isin,
                    'Typ': typ
                    })

    context = viewcore.generate_transactional_context('add_depotwert')
    context['approve_title'] = 'Depotwert hinzufügen'

    if post_action_is(request, 'edit'):
        db_index = int(request.values['edit_index'])
        db_row = database_instance().depotwerte.get(db_index)

        default_item = {
            'edit_index': str(db_index),
            'name': db_row['Name'],
            'isin': db_row['ISIN'],
            'typ': db_row['Typ']
        }

        context['default_item'] = default_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['approve_title'] = 'Depotwert aktualisieren'

    if 'default_item' not in context:
        context['default_item'] = {
            'name': '',
            'isin': '',
            'typ': database_instance().depotwerte.TYP_ETF
        }

    context['letzte_erfassung'] = reversed(non_persisted_state.get_changed_depotwerte())
    context['types'] = database_instance().depotwerte.TYPES
    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'sparen/add_depotwert.html')

