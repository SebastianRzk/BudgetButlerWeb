from django.shortcuts import redirect
from viewcore import viewcore
from test import DBManagerStub
from viewcore import configuration_provider
# Create your views here.
def leave_debug(request):
    viewcore.switch_database_instance(request.GET['database'])
    return redirect('/dashboard/')

def enter_testmode(request):
    DBManagerStub.setup_db_for_test()
    configuration_provider.stub_me('''
    PARTNERNAME:Maureen
    ''')
    print('WARNUNG: ENTERING TESTMODE')
    return redirect('/dashboard/')

