from butler_offline.views.core import backup
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.core.database import Database
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.core.database_manager import convert_database_to_multipart_csv
from butler_offline.viewcore import routes
import datetime


def test_should_save_a_database():
    filesystem_stub = FileSystemStub()
    database = Database(name='TestDatabase')
    expected_db_string = convert_database_to_multipart_csv(database=database)
    now = datetime.datetime.strptime('31/01/22 23:59:59.999999', '%d/%m/%y %H:%M:%S.%f')
    context = backup.BackupContext(
        database=database,
        filesystem=filesystem_stub,
        now=now
    )

    result = backup.handle_request(None, context)

    assert filesystem_stub.get_interaction_count() == 1
    backup_path = './Backups/Backup_TestDatabase_2022-01-31 23:59:59.999999.multipart_csv'
    assert filesystem_stub.get_all_files() == [backup_path]
    assert filesystem_stub.get_raw_file(backup_path) == expected_db_string
    assert not result.is_transactional()
    assert result.is_redirect()
    assert result.redirect_target_url() == routes.CORE_CONFIGURATION + '?success_message=Backup erstellt'


def test_index_should_be_secured_by_request_handler():
    def handle():
        backup.index(request=GetRequest())

    result = run_in_mocked_handler(handle)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['']
