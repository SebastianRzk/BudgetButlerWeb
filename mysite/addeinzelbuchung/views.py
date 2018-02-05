
from viewcore import viewcore
from viewcore.viewcore import post_action_is
from viewcore import request_handler
from viewcore.converter import datum, dezimal_float, datum_to_string, \
    from_double_to_german



def handle_request(request):
    context = viewcore.generate_base_context('addeinzelbuchung')
    context['element_titel'] = 'Neue Ausgabe'
    context['approve_title'] = 'Ausgabe hinzufügen'
    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    if request.method == 'POST' and request.POST['action'] == 'add':
        value = dezimal_float(request.POST['wert']) * -1
        if 'edit_index' in request.POST:
            database_index = int(request.POST['edit_index'])
            einzelbuchungen.edit(
                database_index,
                datum(request.POST['date']),
                request.POST['kategorie'],
                request.POST['name'],
                value)
            viewcore.add_changed_einzelbuchungen(
                {
                    'fa':'pencil',
                    'datum':request.POST['date'],
                    'kategorie':request.POST['kategorie'],
                    'name':request.POST['name'],
                    'wert':from_double_to_german(value)
                    })
        else:
            einzelbuchungen.add(
                datum(request.POST['date']),
                request.POST['kategorie'],
                request.POST['name'],
                value)

            viewcore.add_changed_einzelbuchungen(
                {
                    'fa':'plus',
                    'datum':request.POST['date'],
                    'kategorie':request.POST['kategorie'],
                    'name':request.POST['name'],
                    'wert':from_double_to_german(value)
                    })


        viewcore.save_database()
    if post_action_is(request, 'edit'):
        print('Please edit:', request.POST['edit_index'])
        db_index = int(request.POST['edit_index'])

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


    context['transaction_key'] = 'requested'
    context['kategorien'] = sorted(einzelbuchungen.get_kategorien_ausgaben())
    context['letzte_erfassung'] = reversed(viewcore.get_changed_einzelbuchungen())
    return context

def index(request):
    return request_handler.handle_request(request, handle_request, 'addeinzelbuchung.html')
