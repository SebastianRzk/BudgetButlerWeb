
from viewcore import viewcore
from viewcore import request_handler
from viewcore.converter import datum, dezimal_float, datum_to_string, from_double_to_german


def handle_request(request):
    if request.method == 'POST' and request.POST['action'] == 'add':
        value = dezimal_float(request.POST['wert'])
        if request.POST['typ'] == 'Ausgabe':
            value = value * -1

        if 'edit_index' in request.POST:
            viewcore.database_instance().dauerauftraege.edit(
                int(request.POST['edit_index']),
                datum(request.POST['startdatum']),
                datum(request.POST['endedatum']),
                request.POST['kategorie'],
                request.POST['name'],
                request.POST['rhythmus'],
                value)
            viewcore.add_changed_dauerauftraege({
                'fa': 'pencil',
                'startdatum': str(datum(request.POST['startdatum'])),
                'endedatum':  str(datum(request.POST['endedatum'])),
                'kategorie': request.POST['kategorie'],
                'name': request.POST['name'],
                'rhythmus': request.POST['rhythmus'],
                'wert': from_double_to_german(value)
                })
        else:
            viewcore.database_instance().dauerauftraege.add(
                datum(request.POST['startdatum']),
                datum(request.POST['endedatum']),
                request.POST['kategorie'],
                request.POST['name'],
                request.POST['rhythmus'],
                value)
            viewcore.add_changed_dauerauftraege({
                'fa': 'plus',
                'startdatum': str(datum(request.POST['startdatum'])),
                'endedatum': str(datum(request.POST['endedatum'])),
                'kategorie': request.POST['kategorie'],
                'name': request.POST['name'],
                'rhythmus': request.POST['rhythmus'],
                'wert': from_double_to_german(value)
                })

        viewcore.save_refresh()
    context = viewcore.generate_base_context('adddauerauftrag')
    context['approve_title'] = 'Dauerauftrag hinzufügen'

    if request.method == 'POST' and request.POST['action'] == 'edit':
        db_index = int(request.POST['edit_index'])
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

    context['transaction_key'] = 'requested'
    context['kategorien'] = sorted(viewcore.database_instance().einzelbuchungen.get_alle_kategorien())
    context['letzte_erfassung'] = reversed(viewcore.get_changed_dauerauftraege())
    context['rhythmen'] = ['monatlich']
    return context

def index(request):
    return request_handler.handle_request(request, handle_request, 'theme/adddauerauftrag.html')
