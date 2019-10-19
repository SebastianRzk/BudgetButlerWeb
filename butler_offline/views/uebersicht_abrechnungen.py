from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.converter import datum_to_german


def _handle_request(request):
    zusammenfassungen = [
        {
            'name': 'Zusammenfassung 2019',
            'jahr': '2019',
            'monate': [1, 0, 2, 0, 0, 40, 0, 0, 3, 10, 0, 30]
        }

    ]

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

    context = viewcore.generate_transactional_context('uebersichtabrechnungen')
    context['zusammenfassungen'] = zusammenfassungen
    context['abrechnungen'] = abrechnungen
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'uebersicht_abrechnungen.html')
