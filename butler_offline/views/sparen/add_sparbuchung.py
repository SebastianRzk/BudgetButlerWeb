from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.converter import from_double_to_german, datum, datum_to_string, datum_to_german
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import non_persisted_state

EIGENSCHAFT = 'eigenschaft'
EIGENSCHAFTEN = 'eigenschaften'
EIGENSCHAFT_EINZAHLUNG = 'Einzahlung'
EIGENSCHAFT_AUSZAHLUNG = 'Auszahlung'

def handle_request(request):
    if post_action_is(request, 'add'):
        date = datum(request.values['date'])
        value = request.values['wert'].replace(",", ".")
        value = float(value)

        if request.values[EIGENSCHAFT] == EIGENSCHAFT_AUSZAHLUNG:
            value = value * -1

        if "edit_index" in request.values:
            database_instance().sparbuchungen.edit(int(request.values['edit_index']),
                datum=date,
                name=request.values['name'],
                wert="%.2f" % value,
                typ=request.values['typ'],
                konto=request.values['konto'])
            non_persisted_state.add_changed_sparbuchungen(
                {
                    'fa': 'pencil',
                    'datum': datum_to_german(date),
                    'wert': from_double_to_german(value),
                    'name': request.values['name'],
                    'typ': request.values['typ'],
                    'konto': request.values['konto']
                })

        else:
            database_instance().sparbuchungen.add(
                datum=date,
                name=request.values['name'],
                wert="%.2f" % value,
                typ=request.values['typ'],
                konto=request.values['konto'])
            non_persisted_state.add_changed_sparbuchungen(
                {
                    'fa': 'plus',
                    'datum': datum_to_german(date),
                    'wert': from_double_to_german(value),
                    'name': request.values['name'],
                    'typ': request.values['typ'],
                    'konto': request.values['konto']
                    })

    context = viewcore.generate_transactional_context("add_sparbuchung")
    context['approve_title'] = 'Sparbuchung hinzufügen'
    if post_action_is(request, 'edit'):
        print("Please edit:", request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        db_row = database_instance().sparbuchungen.get(db_index)

        if db_row['Wert'] > 0:
            eigenschaft = EIGENSCHAFT_EINZAHLUNG
        else:
            eigenschaft = EIGENSCHAFT_AUSZAHLUNG

        default_item = {
            'edit_index': str(db_index),
            'datum': datum_to_string(db_row['Datum']),
            'name': db_row['Name'],
            'wert': from_double_to_german(abs(db_row['Wert'])),
            'typ': db_row['Typ'],
            'eigenschaft': eigenschaft,
            'konto': db_row['Konto']
        }

        context['default_item'] = default_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['approve_title'] = 'Sparbuchung aktualisieren'

    if 'default_item' not in context:
        context['default_item'] = {
            'name': '',
            'wert': '',
            'datum': '',
            'typ': '',
            'konto': ''
        }

    context['kontos'] = ['Demo Konto 1']
    context['typen'] = [database_instance().sparbuchungen.TYP_MANUELLER_AUFTRAG]
    context['eigenschaften'] = [EIGENSCHAFT_EINZAHLUNG, EIGENSCHAFT_AUSZAHLUNG]
    context['letzte_erfassung'] = reversed(non_persisted_state.get_changed_sparbuchungen())
    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'sparen/add_sparbuchung.html')

