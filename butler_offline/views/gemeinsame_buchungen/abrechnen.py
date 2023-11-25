from datetime import datetime

from butler_offline.core import file_system
from butler_offline.core.database import Database
from butler_offline.core.time import time
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context
from butler_offline.viewcore.converter import datum_from_german
from butler_offline.viewcore.http import Request


class AbrechnenContext:
    def __init__(self,
                 database: Database,
                 now: datetime,
                 filesystem: file_system.FileSystemImpl
                 ):
        self._database = database
        self._filesystem = filesystem
        self._now = now

    def database(self) -> Database:
        return self._database

    def now(self) -> datetime:
        return self._now

    def filesystem(self) -> file_system.FileSystemImpl:
        return self._filesystem


def handle_request(request: Request, context: AbrechnenContext):
    result_context = generate_transactional_page_context('gemeinsamabrechnen')

    set_mindate = datum_from_german(request.values['set_mindate'])
    set_maxdate = datum_from_german(request.values['set_maxdate'])
    set_self_kategorie = request.get_post_parameter_or_default('set_self_kategorie', None)
    set_other_kategorie = request.get_post_parameter_or_default('set_other_kategorie', None)

    abrechnungs_text = context.database().abrechnen(
        now=context.now(),
        filesystem=context.filesystem(),
        mindate=set_mindate,
        maxdate=set_maxdate,
        set_ergebnis=request.values['set_ergebnis'],
        verhaeltnis=int(request.values['set_verhaeltnis']),
        set_self_kategorie=set_self_kategorie,
        set_other_kategorie=set_other_kategorie
    )
    result_context.add('abrechnungstext', abrechnungs_text.replace('\n', '<br>'))

    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='shared/present_abrechnung.html',
        context_creator=lambda db: AbrechnenContext(
            database=db,
            now=time.now(),
            filesystem=file_system.instance()
        )
    )
