
from mysite.viewcore import viewcore
from mysite.viewcore.viewcore import post_action_is
from mysite.viewcore import request_handler
from mysite.viewcore.converter import datum, dezimal_float, datum_to_string, from_double_to_german, datum_to_german


def handle_request(request):
    if request.method == 'POST' and request.values['action'] == 'add':
        value = dezimal_float(request.values['wert'])
        if request.values['typ'] == 'Ausgabe':
            value = value * -1

        if 'edit_index' in request.values:
            startdatum = datum(request.values['startdatum'])
            endedatum = datum(request.values['endedatum'])
            viewcore.database_instance().dauerauftraege.edit(
                int(request.values['edit_index']),
                startdatum,
                endedatum,
                request.values['kategorie'],
                request.values['name'],
                request.values['rhythmus'],
                value)
            viewcore.add_changed_dauerauftraege({
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
            viewcore.database_instance().dauerauftraege.add(
                startdatum,
                endedatum,
                request.values['kategorie'],
                request.values['name'],
                request.values['rhythmus'],
                value)
            viewcore.add_changed_dauerauftraege({
                'fa': 'plus',
                'startdatum': datum_to_german(startdatum),
                'endedatum': datum_to_german(endedatum),
                'kategorie': request.values['kategorie'],
                'name': request.values['name'],
                'rhythmus': request.values['rhythmus'],
                'wert': from_double_to_german(value)
                })

    context = viewcore.generate_base_context('adddauerauftrag')
    context['approve_title'] = 'Dauerauftrag hinzufügen'

    if post_action_is(request, 'edit'):
        db_index = int(request.values['edit_index'])
        default_item = viewcore.database_instance().dauerauftraege.get(db_index)
        default_item['Startdatum'] = datum_to_string(default_item['Startdatum'])
        default_item['Endedatum'] = datum_to_string(default_item['Endedatum'])

        if default_item['Wert'] < 0:
            default_item['typ'] = 'Ausgabe'
        else:
            default_item['typ'] = 'Einnahme'

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
            'typ': 'Ausgabe',
            'Wert': '',
            'Name': ''
        }

    context['transaction_key'] = 'requested'
    context['kategorien'] = sorted(viewcore.database_instance().einzelbuchungen.get_alle_kategorien(hide_ausgeschlossene_kategorien=True))
    context['letzte_erfassung'] = reversed(viewcore.get_changed_dauerauftraege())
    context['rhythmen'] = ['monatlich']
    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'adddauerauftrag.html')
