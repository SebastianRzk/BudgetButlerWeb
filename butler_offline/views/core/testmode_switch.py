from flask import redirect

from butler_offline.core import time
from butler_offline.viewcore import viewcore
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.core import file_system
from butler_offline.viewcore import configuration_provider
from butler_offline.viewcore.converter import datum_from_german as datum


def leave_debug(request):
    viewcore.switch_database_instance(request.args['database'])
    time.reset_viewcore_stubs()
    return redirect('/', code=301)

def enter_testmode(request):
    file_system.INSTANCE = FileSystemStub()
    viewcore.DATABASE_INSTANCE = None
    viewcore.DATABASES = ['test']
    viewcore.CONTEXT = {}
    configuration_provider.LOADED_CONFIG = None
    configuration_provider.set_configuration('PARTNERNAME', 'Maureen')
    time.stub_today_with(datum('22.01.2019'))
    print('WARNUNG: ENTERING TESTMODE')
    return redirect('/', code=301)

