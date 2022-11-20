from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.converter import from_double_to_german, datum, datum_to_string, datum_to_german
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.context import generate_transactional_context

def handle_request(request):
    if post_action_is(request, 'add'):
        date = datum(request.values['date'])
        value = request.values['wert'].replace(",", ".")
        value = float(value)
        value = value * -1
        if "edit_index" in request.values:
            database_instance().gemeinsamebuchungen.edit(int(request.values['edit_index']),
                   datum=date,
                   name=str(request.values['name']),
                   kategorie=request.values['kategorie'],
                   wert=value,
                   person=request.values['person']
                   )
            non_persisted_state.add_changed_gemeinsamebuchungen(
                {
                    'fa': 'pencil',
                    'datum': datum_to_german(date),
                    'kategorie': request.values['kategorie'],
                    'name': request.values['name'],
                    'wert': from_double_to_german(value),
                    'person': request.values['person']
                    })

        else:
            database_instance().gemeinsamebuchungen.add(ausgaben_datum=date,
                  kategorie=request.values['kategorie'],
                  ausgaben_name=request.values['name'],
                  wert="%.2f" % value,
                  person=request.values['person'])
            non_persisted_state.add_changed_gemeinsamebuchungen(
                {
                    'fa': 'plus',
                    'datum': datum_to_german(date),
                    'kategorie': request.values['kategorie'],
                    'name': request.values['name'],
                    'wert': from_double_to_german(value),
                    'person': request.values['person']
                    })

    context = generate_transactional_context("addgemeinsam")
    context['approve_title'] = 'Gemeinsame Ausgabe hinzufügen'
    if post_action_is(request, 'edit'):
        print("Please edit:", request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        db_row = database_instance().gemeinsamebuchungen.get(db_index)
        default_item = {
            'edit_index': str(db_index),
            'datum': datum_to_string(db_row['Datum']),
            'name': db_row['Name'],
            'wert': from_double_to_german(db_row['Wert'] * -1),
            'kategorie': db_row['Kategorie'],
            'person': db_row['Person']
        }

        context['default_item'] = default_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['approve_title'] = 'Gemeinsame Ausgabe aktualisieren'

    if 'default_item' not in context:
        context['default_item'] = {
            'name': '',
            'wert': '',
            'datum': ''
        }

    context['personen'] = [database_instance().name, viewcore.name_of_partner()]
    context['kategorien'] = sorted(database_instance().einzelbuchungen.get_kategorien_ausgaben(hide_ausgeschlossene_kategorien=True))
    context['letzte_erfassung'] = reversed(non_persisted_state.get_changed_gemeinsamebuchungen())
    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'gemeinsame_buchungen/addgemeinsam.html')

