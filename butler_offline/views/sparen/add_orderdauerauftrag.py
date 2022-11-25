from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.converter import from_double_to_german, datum, datum_to_string, datum_to_german
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.core.frequency import ALL_FREQUENCY_NAMES
from butler_offline.views.sparen.language import NO_VALID_DEPOT_IN_DB, NO_VALID_SHARE_IN_DB
from butler_offline.viewcore.context import generate_transactional_context, generate_error_context
from butler_offline.viewcore.template import fa

TYP = 'typ'
TYPEN = 'typen'
TYP_KAUF = 'Kauf'
TYP_VERKAUF = 'Verkauf'


def handle_request(request):
    if not database_instance().sparkontos.get_depots():
        return generate_error_context(
            'add_orderdauerauftrag',
            NO_VALID_DEPOT_IN_DB)

    if not database_instance().depotwerte.get_depotwerte():
        return generate_error_context('add_orderdauerauftrag', NO_VALID_SHARE_IN_DB)

    if post_action_is(request, 'add'):
        startdatum = datum(request.values['startdatum'])
        endedatum = datum(request.values['endedatum'])
        value = request.values['wert'].replace(",", ".")
        value = float(value)

        if request.values[TYP] == TYP_VERKAUF:
            value = value * -1

        if "edit_index" in request.values:
            database_instance().orderdauerauftrag.edit(
                int(request.values['edit_index']),
                startdatum=startdatum,
                endedatum=endedatum,
                rhythmus=request.values['rhythmus'],
                name=request.values['name'],
                wert="%.2f" % value,
                depotwert=request.values['depotwert'],
                konto=request.values['konto'])
            non_persisted_state.add_changed_orderdauerauftrag(
                {
                    'fa': fa.pencil,
                    'startdatum': datum_to_german(startdatum),
                    'endedatum': datum_to_german(endedatum),
                    'rhythmus': request.values['rhythmus'],
                    'wert': from_double_to_german(abs(value)),
                    'name': request.values['name'],
                    TYP: request.values[TYP],
                    'depotwert': request.values['depotwert'],
                    'konto': request.values['konto']
                })

        else:
            database_instance().orderdauerauftrag.add(
                startdatum=startdatum,
                endedatum=endedatum,
                rhythmus=request.values['rhythmus'],
                name=request.values['name'],
                wert="%.2f" % value,
                depotwert=request.values['depotwert'],
                konto=request.values['konto'])
            non_persisted_state.add_changed_orderdauerauftrag(
                {
                    'fa': fa.plus,
                    'startdatum': datum_to_german(startdatum),
                    'endedatum': datum_to_german(endedatum),
                    'rhythmus': request.values['rhythmus'],
                    'wert': from_double_to_german(value),
                    'name': request.values['name'],
                    TYP: request.values[TYP],
                    'value': '%.2f' % abs(value),
                    'depotwert': request.values['depotwert'],
                    'konto': request.values['konto']
                    })

    context = generate_transactional_context('add_orderdauerauftrag')
    context['approve_title'] = 'Order-Dauerauftrag hinzufügen'
    if post_action_is(request, 'edit'):
        print("Please edit:", request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        db_row = database_instance().orderdauerauftrag.get(db_index)

        if db_row['Wert'] > 0:
            typ = TYP_KAUF
        else:
            typ = TYP_VERKAUF

        default_item = {
            'edit_index': str(db_index),
            'startdatum': datum_to_string(db_row['Startdatum']),
            'endedatum': datum_to_string(db_row['Endedatum']),
            'rhythmus': db_row['Rhythmus'],
            'name': db_row['Name'],
            'wert': from_double_to_german(abs(db_row['Wert'])),
            'depotwert': db_row['Depotwert'],
            'typ': typ,
            'konto': db_row['Konto']
        }

        context['default_item'] = default_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['approve_title'] = 'Order-Dauerauftrag aktualisieren'

    if 'default_item' not in context:
        context['default_item'] = {
            'name': '',
            'wert': '',
            'startdatum': '',
            'endedatum': '',
            'rhythmus': 'monatlich',
            'depotwert': '',
            'konto': ''
        }

    context['kontos'] = database_instance().sparkontos.get_depots()
    context[TYPEN] = [TYP_KAUF, TYP_VERKAUF]
    context['rhythmen'] = ALL_FREQUENCY_NAMES
    context['depotwerte'] = database_instance().depotwerte.get_depotwerte_descriptions()
    context['letzte_erfassung'] = reversed(non_persisted_state.get_changed_orderdauerauftrag())
    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'sparen/add_orderdauerauftrag.html')
