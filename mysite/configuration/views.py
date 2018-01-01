from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore
from viewcore import request_handler

def _handle_request(request):
    if request.method == 'POST'and request.POST['action'] == 'edit_databases':
        dbs = request.POST['dbs']

        all_lines = []
        file = open('../config', 'r')
        for line in file:
            line = line.strip()
            all_lines.append(line)

        file = open('../config', 'w')
        for line in all_lines:
            if line.startswith('DATABASES:'):
                file.write('DATABASES:' + dbs + '\n')
            else:
                file.write(line + '\n')
        file.close()

        viewcore.DATABASES = []
        viewcore.database_instance()

    if request.method == 'POST'and request.POST['action'] == 'add_kategorie':
        viewcore.database_instance().einzelbuchungen.add_kategorie(request.POST['neue_kategorie'])

    context = viewcore.generate_base_context('configuration')
    default_databases = ''
    for db in viewcore.DATABASES:
        if len(default_databases) != 0:
            default_databases = default_databases + ','
        default_databases = default_databases + db
    context['default_databases'] = default_databases
    return context

def index(request):
    return request_handler.handle_request(request, _handle_request, 'theme/konfiguration.html')

