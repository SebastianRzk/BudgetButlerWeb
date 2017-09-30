from django.shortcuts import redirect
from viewcore import viewcore

# Create your views here.
def leave_debug(request):
    viewcore.switch_database_instance(request.GET['database'])
    return redirect("/dashboard/")