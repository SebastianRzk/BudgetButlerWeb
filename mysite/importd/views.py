from _io import StringIO
import datetime

from django.shortcuts import render
from django.template.loader import render_to_string
import pandas

from viewcore import viewcore


def __init__(self):
    self.count = 0



def _mapping_passt(post_parameter, unpassende_kategorien):
    for unpassenden_kategorie in unpassende_kategorien:
        if not str(unpassenden_kategorie) + "_mapping" in post_parameter:
            return False
    return True

def _import(import_data):
    print('importing data:')
    print(import_data)
    viewcore.database_instance().einzelbuchungen.parse(import_data)
    viewcore.save_refresh()

def _map_kategorien(import_data, unpassende_kategorien, post_parameter):
    print('Mappe Kategorien', unpassende_kategorien, post_parameter)

    for unpassende_kategorie in unpassende_kategorien:
        mapping_string = post_parameter[str(unpassende_kategorie) + '_mapping']
        if mapping_string == 'neue Kategorie anlegen':
            print(unpassende_kategorie, ' muss nicht gemappt werden')
            continue
        mapping_kategorie = mapping_string[4:len(' importieren') * -1]
        print(unpassende_kategorie, 'wird in', mapping_kategorie, 'gemappt')
        import_data.Kategorie = import_data.Kategorie.map(lambda x: _kategorien_map(x, unpassende_kategorie, mapping_kategorie))
    return import_data


def index(request):
    renderpage, context = handle_request(request)
    rendered_content = render_to_string('theme/' + renderpage, context, request=request)
    context['content'] = rendered_content
    return render(request, 'theme/index.html', context)


def handle_request(request):
    print(request)
    imported_values = pandas.DataFrame([], columns=('Datum', 'Kategorie', 'Name', 'Wert', ''))
    if request.method == "POST":
        print(request.POST)
        tables = {}

        tables["sonst"] = ""
        tables["#######MaschinenimportStart"] = ""
        mode = "sonst"
        content = request.POST['import'].replace('\r', '')
        print('textfield content:', request.POST['import'].replace('\r', ''))
        for line in content.split('\n'):
            print(line)
            line = line.strip()
            if line == "":
                continue
            if line == "#######MaschinenimportStart":
                mode = "#######MaschinenimportStart"
                continue

            if line == "#######MaschinenimportEnd":
                mode = "sonst"
                continue
            tables[mode] = tables[mode] + "\n" + line


        print(tables)

        imported_values = pandas.read_csv(StringIO(tables["#######MaschinenimportStart"]))
        datenbank_kategorien = set(viewcore.database_instance().einzelbuchungen.get_alle_kategorien())
        nicht_passende_kategorien = []
        for imported_kategorie in set(imported_values.Kategorie):
            if imported_kategorie not in datenbank_kategorien:
                nicht_passende_kategorien.append(imported_kategorie)




        if not nicht_passende_kategorien:
            print('keine unpassenden kategorien gefunden')
            print('beginne mit dem direkten import')
            _import(imported_values)

            context = viewcore.generate_base_context('import')
            last_elements = []
            for row_index, row in imported_values.iterrows():
                last_elements.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))
            context['ausgaben'] = last_elements

            return 'import.html', context

        elif _mapping_passt(request.POST, nicht_passende_kategorien):
            print('import kann durchgeführt werden, weil mapping vorhanden')
            imported_values = _map_kategorien(imported_values, nicht_passende_kategorien, request.POST)
            _import(imported_values)

            context = viewcore.generate_base_context('import')
            last_elements = []
            for row_index, row in imported_values.iterrows():
                last_elements.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))
            context['ausgaben'] = last_elements

            return 'import.html', context


        print("Nicht passende Kategorien: ", nicht_passende_kategorien)
        options = ['neue Kategorie anlegen']

        for kategorie_option in datenbank_kategorien:
            options.append('als ' + str(kategorie_option) + ' importieren')
        options = sorted(options)
        options.insert(0, 'neue Kategorie anlegen')
        context = viewcore.generate_base_context('import')
        context['unpassende_kategorien'] = nicht_passende_kategorien
        context['optionen'] = options
        context['import'] = request.POST['import']
        context['ID'] = viewcore.get_next_transaction_id()
        return 'import_mapping.html', context

    return 'import.html', viewcore.generate_base_context('import')

def _kategorien_map(actual, target, goal):
    if actual != target:
        return actual
    return goal

def _base_import_site(request, context):
    rendered_content = render_to_string('theme/import.html', context, request=request)
    context['content'] = rendered_content
    return render(request, 'theme/index.html', context)
