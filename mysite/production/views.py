from django.shortcuts import redirect
from viewcore import viewcore
from test import DBManagerStub
# Create your views here.
def leave_debug(request):
    print(request.GET.url)
    viewcore.switch_database_instance(request.GET['database'])
    return redirect('/dashboard/')

def enter_testmode(request):
    DBManagerStub.setup_db_for_test()
    print('WARNUNG: ENTERING TESTMODE')
    return redirect('/dashboard/')

