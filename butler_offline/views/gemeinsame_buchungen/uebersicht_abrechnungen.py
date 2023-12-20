from butler_offline.viewcore import request_handler
from butler_offline.core.export.text_report import TextReportReader
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core import file_system
from butler_offline.core.file_system import all_abrechnungen, FileSystemImpl
from butler_offline.viewcore.context.builder import generate_page_context
from butler_offline.viewcore.http import Request


class UbersichtAbrechnungenContext:
    def __init__(self, filesystem: FileSystemImpl):
        self._filesystem = filesystem

    def filesystem(self) -> FileSystemImpl:
        return self._filesystem


def handle_request(_: Request, context: UbersichtAbrechnungenContext):

    all_files = all_abrechnungen(filesystem=context.filesystem())

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

    result_context = generate_page_context('uebersichtabrechnungen')
    result_context.add('zusammenfassungen', zusammenfassungen)
    result_context.add('abrechnungen', abrechnungen)
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='gemeinsame_buchungen/uebersicht_abrechnungen.html',
        context_creator=lambda db: UbersichtAbrechnungenContext(
            filesystem=file_system.instance()
        )
    )
