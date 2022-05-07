from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum, dezimal_float, datum_to_string, from_double_to_german, datum_to_german
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.core.frequency import ALL_FREQUENCY_NAMES

TYP_AUSGABE = 'Ausgabe'
TYPE_EINNAHME = 'Einnahme'

def handle_request(request):
    if request.method == 'POST' and request.values['action'] == 'add':
        value = dezimal_float(request.values['wert'])
        if request.values['typ'] == TYP_AUSGABE:
            value = value * -1

        if 'edit_index' in request.values:
            startdatum = datum(request.values['startdatum'])
            endedatum = datum(request.values['endedatum'])
            database_instance().dauerauftraege.edit(
                int(request.values['edit_index']),
                startdatum,
                endedatum,
                request.values['kategorie'],
                request.values['name'],
                request.values['rhythmus'],
                value)
            non_persisted_state.add_changed_dauerauftraege({
                'fa': 'pencil',
                'startdatum': datum_to_german(startdatum),
                'endedatum':  datum_to_german(endedatum),
                'kategorie': request.values['kategorie'],
                'name': request.values['name'],
                'rhythmus': request.values['rhythmus'],
                'wert': from_double_to_german(value)
                })
        else:
            startdatum = datum(request.values['startdatum'])
            endedatum = datum(request.values['endedatum'])
            database_instance().dauerauftraege.add(
                startdatum,
                endedatum,
                request.values['kategorie'],
                request.values['name'],
                request.values['rhythmus'],
                value)
            non_persisted_state.add_changed_dauerauftraege({
                'fa': 'plus',
                'startdatum': datum_to_german(startdatum),
                'endedatum': datum_to_german(endedatum),
                'kategorie': request.values['kategorie'],
                'name': request.values['name'],
                'rhythmus': request.values['rhythmus'],
                'wert': from_double_to_german(value)
                })

    context = viewcore.generate_transactional_context('adddauerauftrag')
    context['approve_title'] = 'Dauerauftrag hinzufügen'

    if post_action_is(request, 'edit'):
        db_index = int(request.values['edit_index'])
        default_item = database_instance().dauerauftraege.get(db_index)
        default_item['Startdatum'] = datum_to_string(default_item['Startdatum'])
        default_item['Endedatum'] = datum_to_string(default_item['Endedatum'])
        default_item['Rhythmus'] = default_item['Rhythmus']

        if default_item['Wert'] < 0:
            default_item['typ'] = TYP_AUSGABE
        else:
            default_item['typ'] = TYPE_EINNAHME

        default_item['Wert'] = from_double_to_german(abs(default_item['Wert']))

        context['default_item'] = default_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['approve_title'] = 'Dauerauftrag aktualisieren'
        context['element_titel'] = 'Dauerauftrag bearbeiten'
        context['active_name'] = 'Dauerauftrag bearbeiten'

    if 'default_item' not in context:
        context['default_item'] = {
            'Startdatum': '',
            'Endedatum': '',
            'typ': TYP_AUSGABE,
            'Rhythmus': ALL_FREQUENCY_NAMES[0],
            'Wert': '',
            'Name': ''
        }

    context['kategorien'] = sorted(
        database_instance().einzelbuchungen.get_alle_kategorien(hide_ausgeschlossene_kategorien=True))
    context['letzte_erfassung'] = reversed(non_persisted_state.get_changed_dauerauftraege())
    context['rhythmen'] = ALL_FREQUENCY_NAMES

    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'einzelbuchungen/add_dauerauftrag.html')
