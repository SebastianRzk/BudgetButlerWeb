from butler_offline.viewcore import request_handler
from butler_offline.core.file_system import all_abrechnungen
from butler_offline.core.export.text_report import TextReportReader
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.viewcore.context import generate_transactional_context

def _handle_request(request):

    all_files = all_abrechnungen()

    text_report_reader = TextReportReader()
    all_content = Einzelbuchungen()

    abrechnungen = []

    for file in all_files:
        report = text_report_reader.read(''.join(file['content']))
        all_content.parse(report)
        abrechnungen.append(
            {
                'name': file['name'],
                'content': ''.join(file['content'])
            }
        )


    jahre = all_content.get_jahre()
    zusammenfassungen = []


    for jahr in sorted(jahre):

        year_selection = all_content.select().select_year(jahr)
        monate = []
        for monat in range(1, 13):
            monate.append(year_selection.select_month(monat).count())
        zusammenfassungen.append(
            {
                'jahr': jahr,
                'monate': monate
            }
        )

    context = generate_transactional_context('uebersichtabrechnungen')
    context['zusammenfassungen'] = zusammenfassungen
    context['abrechnungen'] = abrechnungen
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'gemeinsame_buchungen/uebersicht_abrechnungen.html')
