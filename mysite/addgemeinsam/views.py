import datetime
from django.http.response import HttpResponse
import pandas

import addgemeinsam
from viewcore import viewcore
from viewcore.viewcore import post_action_is
from viewcore.converter import from_double_to_german, datum, datum_to_string
from viewcore import request_handler

def handle_request(request):
    if request.method == "POST" and request.POST['action'] == 'add':
        date = datum(request.POST['date'])
        value = request.POST['wert'].replace(",", ".")
        value = float(value)
        value = value * -1
        einnameausgabe = pandas.DataFrame([[date, request.POST['kategorie'], str(request.POST['name']), value, request.POST['person']]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Person'))
        if "edit_index" in request.POST:
            viewcore.database_instance().gemeinsamebuchungen.edit(int(request.POST['edit_index']), einnameausgabe)
            viewcore.add_changed_gemeinsamebuchungen(
                {
                    'fa':'pencil',
                    'datum':request.POST['date'],
                    'kategorie':request.POST['kategorie'],
                    'name':request.POST['name'],
                    'wert':from_double_to_german(value),
                    'person':request.POST['person']
                    })

        else:
            viewcore.database_instance().gemeinsamebuchungen.add(ausgaben_datum=date,
                                                                        kategorie=request.POST['kategorie'],
                                                                        ausgaben_name=request.POST['name'],
                                                                        wert="%.2f" % value,
                                                                        person=request.POST['person'])
            viewcore.add_changed_gemeinsamebuchungen(
                {
                    'fa':'plus',
                    'datum':date,
                    'kategorie':request.POST['kategorie'],
                    'name':request.POST['name'],
                    'wert':from_double_to_german(value),
                    'person':request.POST['person']
                    })

        viewcore.save_refresh()
    context = viewcore.generate_base_context("addgemeinsam")
    context['approve_title'] = 'Gemeinsame Ausgabe hinzufügen'
    if post_action_is(request, 'edit'):
        print("Please edit:", request.POST['edit_index'])
        db_index = int(request.POST['edit_index'])
        db_row = viewcore.database_instance().gemeinsamebuchungen.content.iloc[db_index]
        default_item = {
            'edit_index': str(db_index),
            'datum': datum_to_string(db_row.Datum),
            'name': db_row.Name,
            'wert': from_double_to_german(db_row.Wert * -1),
            'kategorie': db_row.Kategorie,
            'person': db_row.Person
        }

        context['default_item'] = default_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['approve_title'] = 'Gemeinsame Ausgabe aktualisieren'

    context['personen'] = [viewcore.database_instance().name, viewcore.name_of_partner()]
    context['kategorien'] = sorted(viewcore.database_instance().einzelbuchungen.get_kategorien_ausgaben())
    context['letzte_erfassung'] = reversed(viewcore.get_changed_gemeinsamebuchungen())
    context['transaction_key'] = 'requested'
    return context

def index(request):
    return request_handler.handle_request(request, handle_request, 'addgemeinsam.html')

