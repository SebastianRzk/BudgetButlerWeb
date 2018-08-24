
from mysite.viewcore import viewcore
from mysite.viewcore.viewcore import post_action_is
from mysite.viewcore import request_handler
from mysite.viewcore.converter import datum, dezimal_float, from_double_to_german
from mysite.viewcore.converter import datum_to_string


def handle_request(request):
    context = viewcore.generate_base_context('addeinnahme')
    context['element_titel'] = 'Neue Einnahme'
    context['page_subtitle'] = 'Daten der Einnahme:'
    context['approve_title'] = 'Einnahme hinzufügen'
    einzelbuchungen = viewcore.database_instance().einzelbuchungen

    if post_action_is(request, 'add'):
        if 'edit_index' in request.values:
            einzelbuchungen.edit(
                int(request.values['edit_index']),
                datum(request.values['date']),
                request.values['kategorie'],
                request.values['name'],
                dezimal_float(request.values['wert']))
            viewcore.add_changed_einzelbuchungen(
                {
                    'fa':'pencil',
                    'datum':request.values['date'],
                    'kategorie':request.values['kategorie'],
                    'name':request.values['name'],
                    'wert':from_double_to_german(dezimal_float(request.values['wert']))
                    })

        else:
            einzelbuchungen.add(
                datum(request.values['date']),
                request.values['kategorie'],
                request.values['name'],
                dezimal_float(request.values['wert']))
            viewcore.add_changed_einzelbuchungen(
                {
                    'fa':'plus',
                    'datum':request.values['date'],
                    'kategorie':request.values['kategorie'],
                    'name':request.values['name'],
                    'wert':from_double_to_german(dezimal_float(request.values['wert']))
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

    context['kategorien'] = sorted(einzelbuchungen.get_kategorien_einnahmen())
    context['letzte_erfassung'] = reversed(viewcore.get_changed_einzelbuchungen())
    context['transaction_key'] = 'requested'
    return context


def index(request):
    return request_handler.handle_request(request, handle_request, 'addeinnahme.html')
