
from mysite.viewcore import viewcore
from mysite.viewcore.viewcore import post_action_is
from mysite.viewcore import request_handler
from mysite.viewcore.converter import datum, dezimal_float, datum_to_string, \
    from_double_to_german


def handle_request(request):
    context = viewcore.generate_base_context('addeinzelbuchung')
    context['element_titel'] = 'Neue Ausgabe'
    context['approve_title'] = 'Ausgabe hinzufügen'
    einzelbuchungen = viewcore.database_instance().einzelbuchungen

    if post_action_is(request, 'add'):
        value = dezimal_float(request.values['wert']) * -1
        if 'edit_index' in request.values:
            database_index = int(request.values['edit_index'])
            einzelbuchungen.edit(
                database_index,
                datum(request.values['date']),
                request.values['kategorie'],
                request.values['name'],
                value)
            viewcore.add_changed_einzelbuchungen(
                {
                    'fa':'pencil',
                    'datum':request.values['date'],
                    'kategorie':request.values['kategorie'],
                    'name':request.values['name'],
                    'wert':from_double_to_german(value)
                    })
        else:
            einzelbuchungen.add(
                datum(request.values['date']),
                request.values['kategorie'],
                request.values['name'],
                value)

            viewcore.add_changed_einzelbuchungen(
                {
                    'fa':'plus',
                    'datum':request.values['date'],
                    'kategorie':request.values['kategorie'],
                    'name':request.values['name'],
                    'wert':from_double_to_german(value)
                    })

    if post_action_is(request, 'edit'):
        print('Please edit:', request.values['edit_index'])
        db_index = int(request.values['edit_index'])

        selected_item = einzelbuchungen.get(db_index)
        selected_item['Datum'] = datum_to_string(selected_item['Datum'])
        selected_item['Wert'] = from_double_to_german(selected_item['Wert'] * -1)
        context['default_item'] = selected_item

        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['set_kategorie'] = True
        context['element_titel'] = 'Einzelbuchung bearbeiten'
        context['active_name'] = 'Einzelbuchung bearbeiten'
        context['approve_title'] = 'Ausgabe aktualisieren'

    if 'default_item' not in context:
        context['default_item'] = {
            'Name': '',
            'Datum': '',
            'Wert' : '',
        }

    context['transaction_key'] = 'requested'
    context['kategorien'] = sorted(einzelbuchungen.get_kategorien_ausgaben())
    context['letzte_erfassung'] = reversed(viewcore.get_changed_einzelbuchungen())
    return context

def index(request):
    return request_handler.handle_request(request, handle_request, 'addausgabe.html')
