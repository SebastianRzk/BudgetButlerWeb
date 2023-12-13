from butler_offline.core.database.dauerauftraege import Dauerauftraege
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.frequency import ALL_FREQUENCY_NAMES
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context, TransactionalPageContext
from butler_offline.viewcore.converter import datum, dezimal_float, datum_to_string, from_double_to_german, \
    datum_to_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.state.non_persisted_state.dauerauftraege import (DauerauftragAddedChange,
                                                                              DauerauftragEditiertChange)

TYP_AUSGABE = 'Ausgabe'
TYPE_EINNAHME = 'Einnahme'


class AddDauerauftragContext:

    def __init__(self, dauerauftraege: Dauerauftraege, einzelbuchungen: Einzelbuchungen):
        self._dauerauftraege = dauerauftraege
        self._einzelbuchungen = einzelbuchungen

    def dauerauftraege(self) -> Dauerauftraege:
        return self._dauerauftraege

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen


def handle_request(request: Request, context: AddDauerauftragContext) -> TransactionalPageContext:
    if request.method == 'POST' and request.values['action'] == 'add':
        value = dezimal_float(request.values['wert'])
        if request.values['typ'] == TYP_AUSGABE:
            value = value * -1

        if 'edit_index' in request.values:
            startdatum = datum(request.values['startdatum'])
            endedatum = datum(request.values['endedatum'])
            context.dauerauftraege().edit(
                int(request.values['edit_index']),
                startdatum,
                endedatum,
                request.values['kategorie'],
                request.values['name'],
                request.values['rhythmus'],
                value)
            non_persisted_state.add_changed_dauerauftraege(
                DauerauftragEditiertChange(
                    start_datum=datum_to_german(startdatum),
                    ende_datum=datum_to_german(endedatum),
                    kategorie=request.values['kategorie'],
                    name=request.values['name'],
                    rhythmus=request.values['rhythmus'],
                    wert=Betrag(value)
                ))
        else:
            startdatum = datum(request.values['startdatum'])
            endedatum = datum(request.values['endedatum'])
            context.dauerauftraege().add(
                startdatum,
                endedatum,
                request.values['kategorie'],
                request.values['name'],
                request.values['rhythmus'],
                value)
            non_persisted_state.add_changed_dauerauftraege(DauerauftragAddedChange(
                start_datum=datum_to_german(startdatum),
                ende_datum=datum_to_german(endedatum),
                kategorie=request.values['kategorie'],
                name=request.values['name'],
                rhythmus=request.values['rhythmus'],
                wert=Betrag(value)
            ))

    page_context = generate_transactional_page_context('adddauerauftrag')
    page_context.add('approve_title', 'Dauerauftrag hinzufügen')

    if request.post_action_is('edit'):
        db_index = int(request.values['edit_index'])
        default_item = context.dauerauftraege().get(db_index)
        default_item['Startdatum'] = datum_to_string(default_item['Startdatum'])
        default_item['Endedatum'] = datum_to_string(default_item['Endedatum'])
        default_item['Rhythmus'] = default_item['Rhythmus']

        if default_item['Wert'] < 0:
            default_item['typ'] = TYP_AUSGABE
        else:
            default_item['typ'] = TYPE_EINNAHME

        default_item['Wert'] = from_double_to_german(abs(default_item['Wert']))

        page_context.add('default_item', default_item)
        page_context.add('bearbeitungsmodus', True)
        page_context.add('edit_index', db_index)
        page_context.add('approve_title', 'Dauerauftrag aktualisieren')
        page_context.add('active_name', 'Dauerauftrag bearbeiten')
        page_context.overwrite_page_titel('Dauerauftrag bearbeiten')

    if not page_context.contains('default_item'):
        page_context.add('default_item', {
            'Startdatum': '',
            'Endedatum': '',
            'typ': TYP_AUSGABE,
            'Rhythmus': ALL_FREQUENCY_NAMES[0],
            'Wert': '',
            'Name': ''
        })

    page_context.add('kategorien', sorted(
        context.einzelbuchungen().get_alle_kategorien(hide_ausgeschlossene_kategorien=True)))
    page_context.add('letzte_erfassung', reversed(non_persisted_state.get_changed_dauerauftraege()))
    page_context.add('rhythmen', ALL_FREQUENCY_NAMES)

    return page_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        context_creator=lambda db: AddDauerauftragContext(
            einzelbuchungen=db.einzelbuchungen,
            dauerauftraege=db.dauerauftraege
        ),
        html_base_page='einzelbuchungen/add_dauerauftrag.html'
    )
