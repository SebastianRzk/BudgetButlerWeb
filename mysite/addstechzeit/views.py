

from django.shortcuts import render
from django.template.loader import render_to_string

from addstechzeit import views
from viewcore import viewcore
from viewcore.converter import time, datum

def handle_request(request):

    if request.method == 'POST' and request.POST['action'] == 'add':
        if not viewcore.is_transaction_already_fired(request.POST['ID']):
            viewcore.fire(request.POST['ID'])

            viewcore.database_instance().stechzeiten.add(datum(request.POST['date']), time(request.POST['start']), time(request.POST['ende']), request.POST['arbeitgeber'])
            viewcore.add_changed_stechzeiten({'Datum':datum(request.POST['date']),
                                              'Einstechen':time(request.POST['start']),
                                              'Ausstechen':time(request.POST['ende']),
                                              'Arbeitgeber': request.POST['arbeitgeber']}
                                                               )
            viewcore.save_database()

    if request.method == 'POST' and request.POST['action'] == 'edit':
        if not viewcore.is_transaction_already_fired(request.POST['ID']):
            viewcore.fire(request.POST['ID'])
            viewcore.database_instance().stechzeiten.edit(int(request.POST['edit_index']), datum(request.POST['date']), time(request.POST['start']), time(request.POST['ende']), request.POST['arbeitgeber'])

    if request.method == 'POST' and request.POST['action'] == 'add_sonderzeit':
        if not viewcore.is_transaction_already_fired(request.POST['ID']):
            viewcore.fire(request.POST['ID'])
            item_datum = datum(request.POST['date'])
            item_dauer = time(request.POST['length'])
            item_typ = request.POST['typ']
            item_arbeitgeber = request.POST['arbeitgeber']
            viewcore.database_instance().add_sonder_zeit(item_datum, item_dauer, item_typ, item_arbeitgeber)

    context = viewcore.generate_base_context('addstechzeit')
    context['sonderzeit_typen'] = ['Urlaub', 'Feiertag']
    context['ID'] = viewcore.get_next_transaction_id()
    context['arbeitgeber'] = viewcore.database_instance().get_arbeitgeber()
    context['letzte_erfassung'] = viewcore.get_changed_stechzeiten()
    return context

# Create your views here.
def index(request):
    context = handle_request(request)
    rendered_content = render_to_string('theme/addstechzeit.html', context, request=request)
    context['content'] = rendered_content
    return render(request, 'theme/index.html', context)
