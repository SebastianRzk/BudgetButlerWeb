from _io import StringIO

import pandas
import requests
from datetime import datetime

from mysite.viewcore import viewcore
from mysite.viewcore import request_handler
from mysite.viewcore.viewcore import post_action_is
from mysite.test.RequestStubs import PostRequest
from mysite.test import RequestStubs
from mysite.core import FileSystem
from mysite.viewcore import configuration_provider
from mysite.viewcore import requester


def _mapping_passt(post_parameter, unpassende_kategorien):
    for unpassenden_kategorie in unpassende_kategorien:
        if not str(unpassenden_kategorie) + "_mapping" in post_parameter:
            return False
    return True


def _import(import_data, gemeinsam):
    print('importing data:')
    print(import_data)
    if gemeinsam :
        viewcore.database_instance().gemeinsamebuchungen.parse(import_data)
        viewcore.database_instance().gemeinsamebuchungen.taint()
    else:
        viewcore.database_instance().einzelbuchungen.parse(import_data)
        viewcore.database_instance().einzelbuchungen.taint()


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
    page, context = handle_request(request)
    context['transaction_key'] = 'requested'
    return request_handler.handle_request(request, lambda x: context , page)


def handle_request(request, import_prefix='', gemeinsam=False):
    print(request)
    imported_values = pandas.DataFrame([], columns=('Datum', 'Kategorie', 'Name', 'Wert', ''))
    if request.method == "POST":
        if post_action_is(request, 'load_online_transactions'):
            serverurl = request.values['server']


            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])

            r = requests.post(serverurl + '/getabrechnung.php', data={'email': request.values['email'], 'password': request.values['password']})
            print(r.content)

            response = handle_request(PostRequest({'import' : r.content.decode("utf-8")}), import_prefix='Internet')
            r = requests.post(serverurl + '/deleteitems.php', data={'email': request.values['email'], 'password': request.values['password']})
            return response

        if post_action_is(request, 'load_online_gemeinsame_transactions'):
            serverurl = request.values['server']
            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])
            print(serverurl)

            online_username = requester.instance().post(serverurl + '/getusername.php', data={'email': request.values['email'], 'password': request.values['password']})
            print('online username: ', online_username)
            online_content = requester.instance().post(serverurl + '/getgemeinsam.php', data={'email': request.values['email'], 'password': request.values['password']})
            print(online_content)

            table = _parse_table(online_content)
            print('table before person mapping', table)
            table.Person = table.Person.map(lambda x: viewcore.database_instance().name if x == online_username else configuration_provider.get_configuration('PARTNERNAME'))
            online_content = "#######MaschinenimportStart\n"
            online_content = online_content + table.to_csv(index=False)
            online_content = online_content + "#######MaschinenimportEnd\n"

            response = handle_request(PostRequest({'import' : online_content}), import_prefix='Internet_Gemeinsam', gemeinsam=True)

            requester.instance().post(serverurl + '/deletegemeinsam.php', data={'email': request.values['email'], 'password': request.values['password']})
            return response


        elif post_action_is(request, 'set_kategorien'):
            kategorien = ','.join(sorted(viewcore.database_instance().einzelbuchungen.get_kategorien_ausgaben(hide_ausgeschlossene_kategorien=True)))
            serverurl = request.values['server']

            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])

            serverurl = serverurl + '/setkategorien.php'

            requester.instance().post(serverurl, data={'email': request.values['email'], 'password': request.values['password'], 'kategorien': kategorien})
        else:
            print(request.values)
            content = request.values['import'].replace('\r', '')
            FileSystem.instance().write('../Import/' + import_prefix + 'Import_' + str(datetime.now()), content)

            imported_values = _parse_table(content)
            datenbank_kategorien = set(viewcore.database_instance().einzelbuchungen.get_alle_kategorien())
            nicht_passende_kategorien = []
            for imported_kategorie in set(imported_values.Kategorie):
                if imported_kategorie not in datenbank_kategorien:
                    nicht_passende_kategorien.append(imported_kategorie)

            if 'Person' in imported_values.columns:
                gemeinsam = True

            if not nicht_passende_kategorien:
                print('keine unpassenden kategorien gefunden')
                print('beginne mit dem direkten import')
                _import(imported_values, gemeinsam)

                context = viewcore.generate_base_context('import')
                last_elements = []
                for row_index, row in imported_values.iterrows():
                    last_elements.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))
                context['ausgaben'] = last_elements
                return 'import.html', context

            elif _mapping_passt(request.values, nicht_passende_kategorien):
                print('import kann durchgeführt werden, weil mapping vorhanden')
                imported_values = _map_kategorien(imported_values, nicht_passende_kategorien, request.values)
                _import(imported_values, gemeinsam)

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
            context['element_titel'] = 'Kategorien zuweisen'
            context['unpassende_kategorien'] = nicht_passende_kategorien
            context['optionen'] = options
            context['import'] = request.values['import']
            context['transaction_id'] = 'requested'
            return 'import_mapping.html', context

    context = viewcore.generate_base_context('import')
    context['ONLINE_DEFAULT_SERVER'] = configuration_provider.get_configuration('ONLINE_DEFAULT_SERVER')
    context['ONLINE_DEFAULT_USER'] = configuration_provider.get_configuration('ONLINE_DEFAULT_USER')
    return 'import.html', context

def _kategorien_map(actual, target, goal):
    if actual != target:
        return actual
    return goal

def _add_protokoll_if_needed(serverurl):
    if not serverurl.startswith('http://') and not serverurl.startswith('https://'):
        return 'https://' + serverurl
    return serverurl

def _save_server_creds(serverurl, email):
    configuration_provider.set_configuration('ONLINE_DEFAULT_SERVER', serverurl)
    configuration_provider.set_configuration('ONLINE_DEFAULT_USER', email)

def _parse_table(content):
    tables = {}
    tables["sonst"] = ""
    tables["#######MaschinenimportStart"] = ""
    mode = "sonst"
    print('textfield content:',content)
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

    return pandas.read_csv(StringIO(tables["#######MaschinenimportStart"]))

