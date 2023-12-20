from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context, TransactionalPageContext
from butler_offline.viewcore.converter import datum, dezimal_float, datum_to_string, \
    from_double_to_german, datum_to_german
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.state.non_persisted_state.einzelbuchungen import EinzelbuchungAddedChange, \
    EinzelbuchungEditiertChange
from butler_offline.viewcore.renderhelper import Betrag


class AddAusgabeContext:
    def __init__(self, einzelbuchungen: Einzelbuchungen):
        self._einzelbuchungen = einzelbuchungen

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen


def handle_request(request: Request, context: AddAusgabeContext):
    result_context: TransactionalPageContext = generate_transactional_page_context('addausgabe')
    result_context.add('approve_title', 'Ausgabe hinzufügen')

    if request.post_action_is('add'):
        value = dezimal_float(request.values['wert']) * -1
        if 'edit_index' in request.values:
            database_index = int(request.values['edit_index'])
            datum_object = datum(request.values['date'])
            context.einzelbuchungen().edit(
                index=database_index,
                buchungs_datum=datum_object,
                kategorie=request.values['kategorie'],
                name=request.values['name'],
                wert=value)
            non_persisted_state.add_changed_einzelbuchungen(
                EinzelbuchungEditiertChange(
                    datum=datum_to_german(datum_object),
                    name=request.values['name'],
                    kategorie=request.values['kategorie'],
                    wert=Betrag(value)
                ))
        else:
            datum_object = datum(request.values['date'])
            context.einzelbuchungen().add(
                datum=datum_object,
                kategorie=request.values['kategorie'],
                name=request.values['name'],
                wert=value)

            non_persisted_state.add_changed_einzelbuchungen(
                EinzelbuchungAddedChange(
                    datum=datum_to_german(datum_object),
                    kategorie=request.values['kategorie'],
                    name=request.values['name'],
                    wert=Betrag(value)
                ))

    if request.post_action_is('edit'):
        db_index = int(request.values['edit_index'])

        selected_item = context.einzelbuchungen().get(db_index)
        selected_item['Datum'] = datum_to_string(selected_item['Datum'])
        selected_item['Wert'] = from_double_to_german(selected_item['Wert'] * -1)
        result_context.add('default_item', selected_item)

        result_context.add('bearbeitungsmodus', True)
        result_context.add('edit_index', db_index)
        result_context.add('set_kategorie', True)
        result_context.overwrite_page_titel('Einzelbuchung bearbeiten')
        result_context.add('active_name', 'Einzelbuchung bearbeiten')
        result_context.add('approve_title', 'Ausgabe aktualisieren')

    if not result_context.contains('default_item'):
        result_context.add('default_item', {
            'Name': '',
            'Datum': '',
            'Wert': '',
        })

    result_context.add('kategorien', sorted(context.einzelbuchungen()
                                            .get_kategorien_ausgaben(hide_ausgeschlossene_kategorien=True)))
    result_context.add('letzte_erfassung', reversed(non_persisted_state.get_changed_einzelbuchungen()))
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        context_creator=lambda db: AddAusgabeContext(einzelbuchungen=db.einzelbuchungen),
        html_base_page='einzelbuchungen/add_ausgabe.html'
    )
