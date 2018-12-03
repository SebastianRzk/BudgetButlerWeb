from flask import redirect
from mysite.viewcore import viewcore
from mysite.test.FileSystemStub import FileSystemStub
from mysite.core import FileSystem
from mysite.viewcore import configuration_provider


def leave_debug(request):
    viewcore.switch_database_instance(request.args['database'])
    return redirect('/', code=301)

def enter_testmode(request):
    FileSystem.INSTANCE = FileSystemStub()
    viewcore.DATABASE_INSTANCE = None
    viewcore.DATABASES = ['test']
    viewcore.CONTEXT = {}
    configuration_provider.LOADED_CONFIG = None
    configuration_provider.set_configuration('PARTNERNAME', 'Maureen')
    print('WARNUNG: ENTERING TESTMODE')
    return redirect('/', code=301)

