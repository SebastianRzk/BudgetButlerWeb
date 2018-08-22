from django.shortcuts import redirect
from viewcore import viewcore
from test.FileSystemStub import FileSystemStub
from core import FileSystem
from viewcore import configuration_provider
# Create your views here.
def leave_debug(request):
    viewcore.switch_database_instance(request.GET['database'])
    return redirect('/dashboard/')

def enter_testmode(request):
    FileSystem.INSTANCE = FileSystemStub()
    viewcore.DATABASE_INSTANCE = None
    viewcore.DATABASES = ['test']
    configuration_provider.set_configuration('PARTNERNAME', 'Maureen')
    print('WARNUNG: ENTERING TESTMODE')
    return redirect('/dashboard/')

