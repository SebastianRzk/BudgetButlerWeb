from butler_offline.viewcore import request_handler
from butler_offline.core.file_system import all_abrechnungen
from butler_offline.viewcore import viewcore


def _handle_request(request):

    all_files = all_abrechnungen()
    all_parsed_files = []




    zusammenfassungen = [
        {
            'name': 'Zusammenfassung 2019',
            'jahr': '2019',
            'monate': [1, 0, 2, 0, 0, 40, 0, 0, 3, 10, 0, 30]
        }

    ]
    zusammenfassungen = []

    abrechnungen = [
        {
            'name': 'Abrechnung März 2019',
            'content': '''ABRECHNUNG         2000'''
        },
        {
            'name': 'Abrechnung März 2019',
            'content': '''ABRECHNUNG         2000'''
        }
    ]
    abrechnungen = []

    context = viewcore.generate_transactional_context('uebersichtabrechnungen')
    context['zusammenfassungen'] = zusammenfassungen
    context['abrechnungen'] = abrechnungen
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'uebersicht_abrechnungen.html')
