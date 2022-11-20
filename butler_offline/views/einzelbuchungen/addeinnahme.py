from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum, dezimal_float, from_double_to_german
from butler_offline.viewcore.converter import datum_to_string, datum_to_german
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.context import generate_transactional_context


def handle_request(request):
    context = generate_transactional_context('addeinnahme')
    context['element_titel'] = 'Neue Einnahme'
    context['page_subtitle'] = 'Daten der Einnahme:'
    context['approve_title'] = 'Einnahme hinzufügen'
    einzelbuchungen = persisted_state.database_instance().einzelbuchungen

    if post_action_is(request, 'add'):
        if 'edit_index' in request.values:
            datum_object = datum(request.values['date'])
            einzelbuchungen.edit(
                int(request.values['edit_index']),
                datum_object,
                request.values['kategorie'],
                request.values['name'],
                dezimal_float(request.values['wert']))
            non_persisted_state.add_changed_einzelbuchungen(
                {
                    'fa': 'pencil',
                    'datum': datum_to_german(datum_object),
                    'kategorie': request.values['kategorie'],
                    'name': request.values['name'],
                    'wert': from_double_to_german(dezimal_float(request.values['wert']))
                    })

        else:
            datum_object = datum(request.values['date'])
            einzelbuchungen.add(
                datum_object,
                request.values['kategorie'],
                request.values['name'],
                dezimal_float(request.values['wert']))
            non_persisted_state.add_changed_einzelbuchungen(
                {
                    'fa': 'plus',
                    'datum': datum_to_german(datum_object),
                    'kategorie': request.values['kategorie'],
                    'name': request.values['name'],
                    'wert': from_double_to_german(dezimal_float(request.values['wert']))
                    })

    if post_action_is(request, 'edit'):
        print('Please edit:', request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        selected_item = einzelbuchungen.get(db_index)
        selected_item['Datum'] = datum_to_string(selected_item['Datum'])
        selected_item['Wert'] = from_double_to_german(selected_item['Wert'])
        context['default_item'] = selected_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['set_kategorie'] = True
        context['element_titel'] = 'Einnahme Nr.' + str(db_index) + ' bearbeiten'
        context['page_subtitle'] = 'Daten bearbeiten:'
        context['approve_title'] = 'Einnahme aktualisieren'

    if 'default_item' not in context:
        context['default_item'] = {
            'Datum': '',
            'Name': '',
            'Wert': ''
        }

    context['kategorien'] = sorted(einzelbuchungen.get_kategorien_einnahmen(hide_ausgeschlossene_kategorien=True))
    context['letzte_erfassung'] = reversed(non_persisted_state.get_changed_einzelbuchungen())
    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'einzelbuchungen/addeinnahme.html')
