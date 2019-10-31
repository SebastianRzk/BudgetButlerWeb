
import pandas
from datetime import datetime

from butler_offline.core.FileSystem import write_import
from butler_offline.core.export.JSONToTextMapper import JSONToTextMapper

from butler_offline.viewcore import viewcore
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.base_html import set_success_message
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.viewcore import configuration_provider
from butler_offline.viewcore import requester
from butler_offline.views.online_services.session import get_username
from butler_offline.views.online_services.einzelbuchungen import get_einzelbuchungen
from butler_offline.views.online_services.gemeinsame_buchungen import get_gemeinsame_buchungen
from butler_offline.core.export.JSONReport import JSONReport
from butler_offline.core.export.text_report import TextReportWriter, TextReportReader



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
    return request_handler.handle_request(request, handle_request , 'import.html')

def _get_success_message(last_elements):
    number = len(last_elements)
    if number == 1:
        return '1 Buchung wurde importiert'
    return '{anzahl} Buchungen wurden importiert'.format(anzahl=number)


def handle_request(request, import_prefix='', gemeinsam=False):
    print(request)
    imported_values = pandas.DataFrame([], columns=('Datum', 'Kategorie', 'Name', 'Wert', ''))
    context = viewcore.generate_transactional_context('import')
    if request.method == "POST":
        if post_action_is(request, 'load_online_transactions'):
            serverurl = request.values['server']
            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])

            json_report = get_einzelbuchungen(serverurl, request.values['email'], request.values['password'])
            print(json_report)
            print('Mapping to text report')
            text_report = JSONToTextMapper().map(json_report)
            print(text_report)

            response = handle_request(PostRequest({'import' : text_report}), import_prefix='Internet')
            r = requester.instance().post(serverurl + '/deleteitems.php', data={'email': request.values['email'], 'password': request.values['password']})
            return response

        if post_action_is(request, 'load_online_gemeinsame_transactions'):
            serverurl = request.values['server']
            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])
            print(serverurl)
            online_username = get_username(serverurl, request.values['email'], request.values['password'])
            print('butler_online username: ', online_username)

            online_content = get_gemeinsame_buchungen(serverurl, request.values['email'], request.values['password'])
            print(online_content)
            table = JSONReport().dataframe_from_json_gemeinsam(online_content)

            print('table before person mapping', table)
            table.Person = table.Person.map(lambda x: viewcore.database_instance().name if x == online_username else configuration_provider.get_configuration('PARTNERNAME'))
            online_content = TextReportWriter().generate_report(table)
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
            write_import(import_prefix + 'Import_' + str(datetime.now()), content)

            imported_values = TextReportReader().read(content)
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

                last_elements = []
                for row_index, row in imported_values.iterrows():
                    last_elements.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))
                context['ausgaben'] = last_elements
                context = set_success_message(context, _get_success_message(last_elements))
            elif _mapping_passt(request.values, nicht_passende_kategorien):
                print('import kann durchgeführt werden, weil mapping vorhanden')
                imported_values = _map_kategorien(imported_values, nicht_passende_kategorien, request.values)
                _import(imported_values, gemeinsam)

                last_elements = []
                for row_index, row in imported_values.iterrows():
                    last_elements.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))
                context['ausgaben'] = last_elements
                context = set_success_message(context, _get_success_message(last_elements))
            else:
                print("Nicht passende Kategorien: ", nicht_passende_kategorien)
                options = ['neue Kategorie anlegen']
                for kategorie_option in datenbank_kategorien:
                    options.append('als ' + str(kategorie_option) + ' importieren')
                options = sorted(options)
                options.insert(0, 'neue Kategorie anlegen')
                context['element_titel'] = 'Kategorien zuweisen'
                context['unpassende_kategorien'] = nicht_passende_kategorien
                context['optionen'] = options
                context['import'] = request.values['import']
                context['special_page'] = 'import_mapping.html'

    context['ONLINE_DEFAULT_SERVER'] = configuration_provider.get_configuration('ONLINE_DEFAULT_SERVER')
    context['ONLINE_DEFAULT_USER'] = configuration_provider.get_configuration('ONLINE_DEFAULT_USER')
    return context

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
