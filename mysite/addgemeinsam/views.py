

import datetime

from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.context import RequestContext
from django.template.loader import render_to_string
import pandas

import addgemeinsam
from viewcore import viewcore


LAST_ELEMTENTS = pandas.DataFrame([], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))

def handle_request(request):
    print(viewcore.database_instance())
    if request.method == "POST" and request.POST['action'] == 'add':
        print(request.POST)
        if not viewcore.is_transaction_already_fired(request.POST['ID']):
            viewcore.fire(request.POST['ID'])
            datum = request.POST['date']
            datum = datetime.datetime.strptime(datum, '%d/%m/%Y')
            datum = datum.date()
            value = request.POST['wert'].replace(",", ".")
            value = float(value)
            value = value * -1
            einnameausgabe = pandas.DataFrame([[datum, request.POST['kategorie'], request.POST['name'], value, request.POST['person']]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Person'))
            print(einnameausgabe)
            if "edit_index" in request.POST:
                viewcore.database_instance().edit_gemeinsam(int(request.POST['edit_index']), einnameausgabe)
            else:
                viewcore.database_instance().add_gemeinsame_einnahmeausgabe(ausgaben_datum=datum,
                                                                            kategorie=request.POST['kategorie'],
                                                                            ausgaben_name=request.POST['name'],
                                                                            wert=value,
                                                                            person=request.POST['person'])
            addgemeinsam.views.LAST_ELEMTENTS = addgemeinsam.views.LAST_ELEMTENTS.append(einnameausgabe)
            viewcore.save_database()
    print(viewcore.database_instance().einzelbuchungen)
    context = viewcore.generate_base_context("addgemeinsam")
    context['approve_title'] = 'Gemeinsame Ausgabe hinzufügen'
    if request.method == "POST" and request.POST['action'] == 'edit':
        print("Please edit:", request.POST['edit_index'])
        db_index = int(request.POST['edit_index'])
        db_row = viewcore.database_instance().gemeinsame_buchungen.iloc[db_index]
        tag = db_row.Datum.day
        monat = db_row.Datum.month
        jahr = db_row.Datum.year
        context['default_tag'] = str(tag) + "/" + str(monat) + "/" + str(jahr)
        context['default_name'] = db_row.Name
        context['default_wert'] = str(db_row.Wert * -1).replace(".", ",")
        context['default_kategorie'] = db_row.Kategorie
        context['default_person'] = db_row.Person
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['approve_title'] = 'Gemeinsame Ausgabe aktualisieren'
    last_elements = []
    for row_index, row in addgemeinsam.views.LAST_ELEMTENTS.iterrows():
        last_elements.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert, row.Person))

    context['ID'] = viewcore.get_next_transaction_id()
    context['personen'] = ['Sebastian', 'Maureen']
    context['kategorien'] = sorted(viewcore.database_instance().einzelbuchungen.get_kategorien_ausgaben())
    context['letzte_erfassung'] = reversed(last_elements)
    return context

def index(request):
    context = handle_request(request)
    rendered_content = render_to_string('theme/addgemeinsam.html', context, request=request)
    context['content'] = rendered_content
    return render(request, 'theme/index.html', context)

