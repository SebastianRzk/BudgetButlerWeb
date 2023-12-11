import logging
from datetime import datetime

from butler_offline.core import time
from butler_offline.core.configuration_provider import get_database_backup_path
from butler_offline.core.database import Database
from butler_offline.core.database_manager import convert_database_to_multipart_csv
from butler_offline.core.file_system import FileSystemImpl, instance
from butler_offline.viewcore import request_handler
from butler_offline.viewcore import routes
from butler_offline.viewcore.context.builder import generate_redirect_page_context, PageContext
from butler_offline.viewcore.converter import datetime_to_filesystem_string


class BackupContext:
    def __init__(self, database: Database, now: datetime, filesystem: FileSystemImpl):
        self._database = database
        self._now = now
        self._filesystem = filesystem

    def database(self) -> Database:
        return self._database

    def now(self) -> datetime:
        return self._now

    def filesystem(self) -> FileSystemImpl:
        return self._filesystem


def handle_request(_, context: BackupContext) -> PageContext:
    logging.info('starting to create a database backup')
    backup_file_destination = create_backup_destination(context)
    backup_file_content = convert_database_to_multipart_csv(database=context.database())
    logging.info('database serialized')
    context.filesystem().write(
        file_path=backup_file_destination,
        file_content=backup_file_content
    )
    logging.info('wrote database to %s', backup_file_destination)
    return generate_redirect_page_context(
        redirect_target_url='{}?{}={}'.format(routes.CORE_CONFIGURATION,
                                              routes.CORE_CONFIGURATION_PARAM_SUCCESS_MESSAGE,
                                              'Backup erstellt'))


def create_backup_destination(context):
    backup_file_name = 'Backup_{}_{}.multipart_csv'.format(
        context.database().name,
        datetime_to_filesystem_string(context.now()))
    backup_file_destination = '{}/{}'.format(get_database_backup_path(), backup_file_name)
    return backup_file_destination


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        context_creator=lambda db: BackupContext(
            database=db,
            now=time.now(),
            filesystem=instance()
        ),
        html_base_page=''
    )
