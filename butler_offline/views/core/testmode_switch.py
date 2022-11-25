from flask import redirect

from butler_offline.viewcore.state import persisted_state
from butler_offline.core import time, configuration_provider
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.core import file_system
from butler_offline.viewcore.converter import datum_from_german as datum
import logging


def leave_debug(request):
    persisted_state.switch_database_instance(request.args['database'])
    time.reset_viewcore_stubs()
    return redirect('/', code=301)

def enter_testmode(request):
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    persisted_state.DATABASES = ['test']
    non_persisted_state.CONTEXT = {}
    configuration_provider.LOADED_CONFIG = None
    configuration_provider.set_configuration('PARTNERNAME', 'Partner')
    time.stub_today_with(datum('22.01.2019'))
    logging.warning('WARNUNG: ENTERING TESTMODE')
    return redirect('/', code=301)

