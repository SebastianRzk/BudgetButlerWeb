

from django.shortcuts import render
from django.template.loader import render_to_string

from addstechzeit import views
from viewcore import viewcore
from viewcore.converter import time, datum
from viewcore import request_handler
def handle_request(request):

    if request.method == 'POST' and request.POST['action'] == 'add':
        viewcore.database_instance().stechzeiten.add(datum(request.POST['date']), time(request.POST['start']), time(request.POST['ende']), request.POST['arbeitgeber'])
        viewcore.add_changed_stechzeiten({'Datum':datum(request.POST['date']),
                                          'Einstechen':time(request.POST['start']),
                                          'Ausstechen':time(request.POST['ende']),
                                          'Arbeitgeber': request.POST['arbeitgeber']}
                                                           )
        viewcore.save_database()

    if request.method == 'POST' and request.POST['action'] == 'edit':
        viewcore.database_instance().stechzeiten.edit(int(request.POST['edit_index']), datum(request.POST['date']), time(request.POST['start']), time(request.POST['ende']), request.POST['arbeitgeber'])

    if request.method == 'POST' and request.POST['action'] == 'add_sonderzeit':
        item_datum = datum(request.POST['date'])
        item_dauer = time(request.POST['length'])
        item_typ = request.POST['typ']
        item_arbeitgeber = request.POST['arbeitgeber']
        viewcore.database_instance().sonderzeiten.add(item_datum, item_dauer, item_typ, item_arbeitgeber)

    context = viewcore.generate_base_context('addstechzeit')
    context['sonderzeit_typen'] = ['Urlaub', 'Feiertag']
    context['transaction_key'] = 'requested'
    context['arbeitgeber'] = viewcore.database_instance().get_arbeitgeber()
    context['letzte_erfassung'] = viewcore.get_changed_stechzeiten()
    return context

def index(request):
    return request_handler.handle_request(request, handle_request, 'theme/addstechzeit.html')
