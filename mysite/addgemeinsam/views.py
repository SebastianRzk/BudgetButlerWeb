

import datetime

from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.context import RequestContext
from django.template.loader import render_to_string
import pandas

import addgemeinsam
from viewcore import viewcore
from viewcore.converter import from_double_to_german
from viewcore import request_handler

def handle_request(request):
    print(viewcore.database_instance())
    if request.method == "POST" and request.POST['action'] == 'add':
        print(request.POST)
        datum = request.POST['date']
        datum = datetime.datetime.strptime(datum, '%d/%m/%Y')
        datum = datum.date()
        value = request.POST['wert'].replace(",", ".")
        value = float(value)
        value = value * -1
        einnameausgabe = pandas.DataFrame([[datum, request.POST['kategorie'], request.POST['name'], value, request.POST['person']]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Person'))
        print(einnameausgabe)
        if "edit_index" in request.POST:
            viewcore.database_instance().gemeinsamebuchungen.edit(int(request.POST['edit_index']), einnameausgabe)
            viewcore.add_changed_gemeinsamebuchungen(
                {
                    'fa':'pencil',
                    'datum':str(datum),
                    'kategorie':request.POST['kategorie'],
                    'name':request.POST['name'],
                    'wert':"%.2f" % value,
                    'person':request.POST['person']
                    })

        else:
            viewcore.database_instance().gemeinsamebuchungen.add(ausgaben_datum=datum,
                                                                        kategorie=request.POST['kategorie'],
                                                                        ausgaben_name=request.POST['name'],
                                                                        wert="%.2f" % value,
                                                                        person=request.POST['person'])
            viewcore.add_changed_gemeinsamebuchungen(
                {
                    'fa':'plus',
                    'datum':str(datum),
                    'kategorie':request.POST['kategorie'],
                    'name':request.POST['name'],
                    'wert':"%.2f" % value,
                    'person':request.POST['person']
                    })

        viewcore.save_refresh()
    print(viewcore.database_instance().einzelbuchungen)
    context = viewcore.generate_base_context("addgemeinsam")
    context['approve_title'] = 'Gemeinsame Ausgabe hinzufügen'
    if request.method == "POST" and request.POST['action'] == 'edit':
        print("Please edit:", request.POST['edit_index'])
        db_index = int(request.POST['edit_index'])
        db_row = viewcore.database_instance().gemeinsamebuchungen.content.iloc[db_index]
        tag = db_row.Datum.day
        monat = db_row.Datum.month
        jahr = db_row.Datum.year
        default_item = {
            'datum': str(tag) + "/" + str(monat) + "/" + str(jahr),
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
    return request_handler.handle_request(request, handle_request, 'theme/addgemeinsam.html')

