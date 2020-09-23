from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.converter import from_double_to_german, datum, datum_to_string, datum_to_german
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import non_persisted_state
from datetime import date

KEY_ID = 'depotwert_id_'
KEY_WERT = 'depotwert_wert_'

def to_key(key, depotwert):
    return '{}{}'.format(key, depotwert)

def calculate_filled_items(actual, possible):
    filled_items = []
    for i, element in actual.iterrows():
        isin = element.Depotwert
        filled_items.append(to_item(isin, resolve_description(isin, possible), element.Wert))
    return filled_items

def calculate_empty_items(actual, possible):
    empty = possible.copy()
    for element in possible:
        if element['isin'] in set(actual.Depotwert.tolist()):
            empty.remove(element)

    result = []
    for element in empty:
        result.append(to_item(element['isin'], element['description'], 0))

    return result


def to_item(isin, description, wert):
    return {
        'isin': isin,
        'description': description,
        'wert': wert
    }

def resolve_description(isin, all):
    for element in all:
        if element['isin'] == isin:
            return element['description']
    return None

def handle_request(request):
    if not database_instance().sparkontos.get_depots():
        return viewcore.generate_error_context('add_depotauszug', 'Bitte erfassen Sie zuerst ein Sparkonto vom Typ "Depot".')

    if not database_instance().depotwerte.get_depotwerte():
        return viewcore.generate_error_context('add_depotauszug', 'Bitte erfassen Sie zuerst ein Depotwert.')

    if post_action_is(request, 'add'):
        current_date = datum(request.values['datum'])
        konto = request.values['konto']

        if "edit_index" in request.values:
            for element in request.values:
                if element.startswith(KEY_ID):
                    depotwert = element.replace(KEY_ID, '')
                    db_index = database_instance().depotauszuege.resolve_index(current_date, konto, depotwert)
                    value = request.values[to_key(KEY_WERT, depotwert)].replace(",", ".")
                    value = float(value)

                    if db_index is not None:
                        database_instance().depotauszuege.edit(db_index,
                                                               datum=current_date,
                                                               depotwert=depotwert,
                                                               wert="%.2f" % value,
                                                               konto=konto)
                        non_persisted_state.add_changed_depotauszuege(
                            {
                                'fa': 'pencil',
                                'datum': datum_to_german(current_date),
                                'wert': from_double_to_german(value),
                                'depotwert': depotwert,
                                'konto': konto
                            })
                    else:
                        database_instance().depotauszuege.add(datum=current_date,
                                                              depotwert=depotwert,
                                                              wert="%.2f" % value,
                                                              konto=konto)
                        non_persisted_state.add_changed_depotauszuege(
                            {
                                'fa': 'plus',
                                'datum': datum_to_german(current_date),
                                'wert': from_double_to_german(value),
                                'depotwert': depotwert,
                                'konto': konto
                            })


        else:

            result = database_instance().depotauszuege.get_by(current_date, konto)
            if len(result) > 0:
                return viewcore.generate_error_context('add_depotauszug',
                                                       'Für es besteht bereits ein Kontoauszug für {} am {}'.format(
                                                           konto,
                                                           datum_to_german(current_date)))

            for element in request.values:
                if element.startswith('depotwert_id_'):
                    depotwert = element.replace('depotwert_id_', '')
                    value = request.values[to_key(KEY_WERT, depotwert)].replace(",", ".")
                    value = float(value)

                    database_instance().depotauszuege.add(datum=current_date,
                                                          depotwert=depotwert,
                                                          wert="%.2f" % value,
                                                          konto=konto)
                    non_persisted_state.add_changed_depotauszuege(
                        {
                            'fa': 'plus',
                            'datum': datum_to_german(current_date),
                            'wert': from_double_to_german(value),
                            'depotwert': depotwert,
                            'konto': konto
                            })

    context = viewcore.generate_transactional_context('add_depotauszug')
    context['approve_title'] = 'Depotauszug hinzufügen'

    depotwerte = database_instance().depotwerte.get_depotwerte_descriptions()
    if post_action_is(request, 'edit'):
        print("Please edit:", request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        db_row = database_instance().depotauszuege.get(db_index)

        edit_datum = db_row['Datum']
        edit_konto = db_row['Konto']
        db_row = database_instance().depotauszuege.get_by(edit_datum, edit_konto)

        default_item = [{
            'datum': datum_to_string(edit_datum),
            'konto': edit_konto,
            'filled_items': calculate_filled_items(db_row, depotwerte),
            'empty_items': calculate_empty_items(db_row, depotwerte)
        }]

        context['default_items'] = default_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['approve_title'] = 'Depotauszug aktualisieren'

    if 'default_items' not in context:
        context['default_items'] = []
        for konto in database_instance().sparkontos.get_depots():
            default_datum = database_instance().depotauszuege.get_latest_datum_by(konto)
            if not default_datum:
                default_datum = date.today()

            db_row = database_instance().depotauszuege.get_by(default_datum, konto)
            default_item = {
                'datum': datum_to_string(default_datum),
                'konto': konto,
                'filled_items': calculate_filled_items(db_row, depotwerte),
                'empty_items': calculate_empty_items(db_row, depotwerte)
            }
            context['default_items'].append(default_item)

    context['letzte_erfassung'] = reversed(non_persisted_state.get_changed_depotauszuege())
    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'sparen/add_sparbuchung.html')

