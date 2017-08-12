from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore
from viewcore.converter import datum, dezimal_float, datum_to_string, \
    from_double_to_german

def __init__(self):
    self.count = 0

def handle_request(request):
    context = viewcore.generate_base_context("addeinzelbuchung")
    context['element_titel'] = "Neue Ausgabe"
    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    if request.method == "POST" and request.POST['action'] == 'add':
        print(request.POST)
        if not viewcore.is_transaction_already_fired(request.POST['ID']):
            viewcore.fire(request.POST['ID'])
            value = dezimal_float(request.POST['wert']) * -1
            if "edit_index" in request.POST:
                database_index = int(request.POST['edit_index'])
                einzelbuchungen.edit(
                    database_index,
                    datum(request.POST['date']),
                    request.POST['kategorie'],
                    request.POST['name'],
                    value)
                viewcore.add_changed_einzelbuchungen(
                    {
                        "mode":"Bearbeitet",
                        "index":database_index,
                        "datum":str(datum(request.POST['date'])),
                        "kategorie":request.POST['kategorie'],
                        "name":request.POST['name'],
                        "wert":value
                        })
            else:
                einzelbuchungen.add(
                    datum(request.POST['date']),
                    request.POST['kategorie'],
                    request.POST['name'],
                    value)

                viewcore.add_changed_einzelbuchungen(
                    {
                        "mode":"Hinzugefügt",
                        "index":"no-set",
                        "datum":str(datum(request.POST['date'])),
                        "kategorie":request.POST['kategorie'],
                        "name":request.POST['name'],
                        "wert":value
                        })


            viewcore.save_database()
    if request.method == "POST" and request.POST['action'] == 'edit':
        print("Please edit:", request.POST['edit_index'])
        db_index = int(request.POST['edit_index'])

        selected_item = einzelbuchungen.get(db_index)
        selected_item['Datum'] = datum_to_string(selected_item['Datum'])
        selected_item['Wert'] = from_double_to_german(selected_item['Wert'] * -1)
        context['default_item'] = selected_item

        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['set_kategorie'] = True
        context['element_titel'] = "Einzelbuchung bearbeiten"
        context['active_name'] = "Einzelbuchung bearbeiten"



    context['ID'] = viewcore.get_next_transaction_id()
    context['kategorien'] = sorted(einzelbuchungen.get_kategorien_ausgaben())
    context['letzte_erfassung'] = viewcore.get_changed_einzelbuchungen()
    return context

def index(request):

    context = handle_request(request)

    rendered_content = render_to_string('theme/addeinzelbuchung.html', context, request=request)
    context['content'] = rendered_content
    return render(request, 'theme/index.html', context)
