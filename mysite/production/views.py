from django.shortcuts import redirect
import viewcore

# Create your views here.
def leave_debug(request):
    viewcore.viewcore.switch_database_instance(request.GET['database'])
    return redirect("/dashboard/")