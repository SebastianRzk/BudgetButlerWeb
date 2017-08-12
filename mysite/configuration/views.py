from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore


def __init__(self):
    self.count = 0

def handle_request(request):
    if request.method == "POST"and request.POST['action'] == 'edit_databases':
        dbs = request.POST['dbs']

        all_lines = []
        file = open("../config", "r")
        for line in file:
            line = line.strip()
            all_lines.append(line)

        file = open("../config", "w")
        for line in all_lines:
            if line.startswith("DATABASES:"):
                file.write("DATABASES:" + dbs + "\n")
            else:
                file.write(line + "\n")
        file.close()

        viewcore.DATABASES = []
        viewcore.database_instance()

    if request.method == "POST"and request.POST['action'] == 'add_kategorie':
        viewcore.database_instance().einzelbuchungen.add_kategorie(request.POST['neue_kategorie'])

    context = viewcore.generate_base_context("configuration")

    file = open("../config", "r")
    for line in file:
        line = line.strip()
        if line.startswith("DATABASES:"):
            line = line.replace("DATABASES:", "")
            context['default_databases'] = line
    return context

def index(request):
    context = handle_request(request)

    rendered_content = render_to_string('theme/konfiguration.html', context, request=request)

    context['content'] = rendered_content

    return render(request, 'theme/index.html', context)

