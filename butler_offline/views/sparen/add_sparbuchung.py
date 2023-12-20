from butler_offline.core.database import Kontos
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context
from butler_offline.viewcore.converter import from_double_to_german, datum, datum_to_string, datum_to_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.template import fa
from butler_offline.viewcore.requirements import sparkontos_needed_decorator


EIGENSCHAFT = 'eigenschaft'
EIGENSCHAFTEN = 'eigenschaften'
EIGENSCHAFT_EINZAHLUNG = 'Einzahlung'
EIGENSCHAFT_AUSZAHLUNG = 'Auszahlung'


class AddSparbuchungContext:
    def __init__(self, sparbuchungen: Sparbuchungen, kontos: Kontos):
        self._sparbuchungen = sparbuchungen
        self._kontos = kontos

    def sparbuchungen(self) -> Sparbuchungen:
        return self._sparbuchungen

    def kontos(self) -> Kontos:
        return self._kontos


@sparkontos_needed_decorator()
def handle_request(request: Request, context: AddSparbuchungContext):
    result_context = generate_transactional_page_context('add_sparbuchung')

    if request.post_action_is('add'):
        date = datum(request.values['datum'])
        value = request.values['wert'].replace(",", ".")
        value = float(value)

        if request.values[EIGENSCHAFT] == EIGENSCHAFT_AUSZAHLUNG:
            value = value * -1

        if "edit_index" in request.values:
            context.sparbuchungen().edit(int(request.values['edit_index']),
                datum=date,
                name=request.values['name'],
                wert=value,
                typ=request.values['typ'],
                konto=request.values['konto'])
            non_persisted_state.add_changed_sparbuchungen(
                {
                    'fa': fa.pencil,
                    'datum': datum_to_german(date),
                    'wert': from_double_to_german(value),
                    'name': request.values['name'],
                    'typ': request.values['typ'],
                    'konto': request.values['konto']
                })

        else:
            context.sparbuchungen().add(
                datum=date,
                name=request.values['name'],
                wert=value,
                typ=request.values['typ'],
                konto=request.values['konto'])
            non_persisted_state.add_changed_sparbuchungen(
                {
                    'fa': fa.plus,
                    'datum': datum_to_german(date),
                    'wert': from_double_to_german(value),
                    'name': request.values['name'],
                    'typ': request.values['typ'],
                    'konto': request.values['konto']
                    })

    result_context.add('approve_title', 'Sparbuchung hinzufügen')
    if request.post_action_is('edit'):
        print("Please edit:", request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        db_row = context.sparbuchungen().get(db_index)

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

        result_context.add('default_item', default_item)
        result_context.add('bearbeitungsmodus', True)
        result_context.add('edit_index', db_index)
        result_context.add('approve_title', 'Sparbuchung aktualisieren')

    if not result_context.contains('default_item'):
        result_context.add('default_item', {
            'name': '',
            'wert': '',
            'datum': '',
            'typ': '',
            'konto': ''
        })

    result_context.add('kontos', context.kontos().get_sparfaehige_kontos())
    result_context.add('typen', context.sparbuchungen().AUFTRAGS_TYPEN)
    result_context.add(EIGENSCHAFTEN, [EIGENSCHAFT_EINZAHLUNG, EIGENSCHAFT_AUSZAHLUNG])
    result_context.add('letzte_erfassung', reversed(non_persisted_state.get_changed_sparbuchungen()))
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='sparen/add_sparbuchung.html',
        context_creator=lambda db: AddSparbuchungContext(
            kontos=db.sparkontos,
            sparbuchungen=db.sparbuchungen
        )
    )