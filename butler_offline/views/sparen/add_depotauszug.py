from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.converter import from_double_to_german, datum, datum_to_string, datum_to_german
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.views.sparen.language import NO_VALID_DEPOT_IN_DB, NO_VALID_SHARE_IN_DB
from datetime import date
from butler_offline.viewcore.context import generate_transactional_context, generate_error_context
from butler_offline.viewcore.template import fa
from butler_offline.core.database import Depotauszuege, Kontos, Depotwerte

KEY_WERT = 'wert_'


def calculate_filled_items(actual, possible):
    filled_items = []
    for i, element in actual.iterrows():
        isin = element.Depotwert
        if element.Wert != 0:
            filled_items.append(to_item(isin, resolve_description(isin, possible), element.Wert))
    return filled_items


def calculate_empty_items(possible, filled):
    empty = possible.copy()

    filled_isin = []
    for f in filled:
        filled_isin.append(f['isin'])

    for element in possible:
        if element['isin'] in filled_isin:
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


def resolve_description(isin: str, all_elements) -> str:
    for element in all_elements:
        if element['isin'] == isin:
            return element['description']
    return None


class AddDepotauszugContext:
    def __init__(self, depotauszuege: Depotauszuege, kontos: Kontos, depotwerte: Depotwerte):
        self._depotauszuege = depotauszuege
        self._kontos = kontos
        self._depotwerte = depotwerte

    def depotauszuege(self) -> Depotauszuege:
        return self._depotauszuege

    def kontos(self) -> Kontos:
        return self._kontos

    def depotwerte(self) -> Depotwerte:
        return self._depotwerte


def handle_request(request, context: AddDepotauszugContext):
    if not context.kontos().get_depots():
        return generate_error_context('add_depotauszug', NO_VALID_DEPOT_IN_DB)

    if not context.depotwerte().get_depotwerte():
        return generate_error_context('add_depotauszug', NO_VALID_SHARE_IN_DB)

    if post_action_is(request, 'add'):
        current_date = None
        for element in request.values:
            if element.startswith('datum_'):
                current_date = datum(request.values[element])
        if not current_date:
            return generate_error_context('add_depotauszug', 'Interner Fehler <Kein Datum gefunden>.')
        konto = request.values['konto']

        if "edit_index" in request.values:
            for element in request.values:
                if element.startswith(KEY_WERT):
                    depotwert = element.split('_')[-1]
                    db_index = context.depotauszuege().resolve_index(current_date, konto, depotwert)
                    value = request.values[element].replace(",", ".")
                    value = float(value)

                    if db_index is not None:
                        context.depotauszuege().edit(db_index,
                                                     datum=current_date,
                                                     depotwert=depotwert,
                                                     wert="%.2f" % value,
                                                     konto=konto)
                        non_persisted_state.add_changed_depotauszuege(
                            {
                                'fa': fa.pencil,
                                'datum': datum_to_german(current_date),
                                'wert': from_double_to_german(value),
                                'depotwert': depotwert,
                                'konto': konto
                            })
                    else:
                        context.depotauszuege().add(datum=current_date,
                                                    depotwert=depotwert,
                                                    wert="%.2f" % value,
                                                    konto=konto)
                        non_persisted_state.add_changed_depotauszuege(
                            {
                                'fa': fa.plus,
                                'datum': datum_to_german(current_date),
                                'wert': from_double_to_german(value),
                                'depotwert': depotwert,
                                'konto': konto
                            })


        else:

            result = context.depotauszuege().get_by(current_date, konto)
            if len(result) > 0:
                return generate_error_context('add_depotauszug',
                                              'Für es besteht bereits ein Kontoauszug für {} am {}'.format(
                                                  konto,
                                                  datum_to_german(current_date)))

            for element in request.values:
                if element.startswith(KEY_WERT):
                    depotwert = element.split('_')[-1]
                    value = request.values[element].replace(",", ".")
                    value = float(value)

                    if value == 0 and not context.depotauszuege().exists_wert(konto, depotwert):
                        continue

                    context.depotauszuege().add(datum=current_date,
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

    render_context = generate_transactional_context('add_depotauszug')
    render_context['approve_title'] = 'Depotauszug hinzufügen'

    depotwerte = context.depotwerte().get_depotwerte_descriptions()
    if post_action_is(request, 'edit'):
        print("Please edit:", request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        db_row = context.depotauszuege().get(db_index)

        edit_datum = db_row['Datum']
        edit_konto = db_row['Konto']
        db_row = context.depotauszuege().get_by(edit_datum, edit_konto)

        filled_items = calculate_filled_items(db_row, depotwerte)
        empty_items = calculate_empty_items(depotwerte, filled_items)

        default_item = [{
            'datum': datum_to_string(edit_datum),
            'konto': edit_konto,
            'filled_items': filled_items,
            'empty_items': empty_items
        }]

        render_context['default_items'] = default_item
        render_context['bearbeitungsmodus'] = True
        render_context['edit_index'] = db_index
        render_context['approve_title'] = 'Depotauszug aktualisieren'

    if 'default_items' not in render_context:
        render_context['default_items'] = []
        for konto in context.kontos().get_depots():
            default_datum = context.depotauszuege().get_latest_datum_by(konto)
            if not default_datum:
                default_datum = date.today()

            db_row = context.depotauszuege().get_by(default_datum, konto)

            filled_items = calculate_filled_items(db_row, depotwerte)
            empty_items = calculate_empty_items(depotwerte, filled_items)

            if len(filled_items) == 0:
                filled_items = empty_items
                empty_items = []

            default_item = {
                'datum': datum_to_string(date.today()),
                'konto': konto,
                'filled_items': filled_items,
                'empty_items': empty_items
            }
            render_context['default_items'].append(default_item)

    render_context['letzte_erfassung'] = reversed(non_persisted_state.get_changed_depotauszuege())
    return render_context


from butler_offline.viewcore.state.persisted_state import database_instance


def index(request):
    context = AddDepotauszugContext(depotauszuege=database_instance().depotauszuege,
                                    kontos=database_instance().sparkontos,
                                    depotwerte=database_instance().depotwerte)

    def migration_function(r):
        return handle_request(request=r, context=context)

    return request_handler.handle_request(request, migration_function, 'sparen/add_depotauszug.html')
