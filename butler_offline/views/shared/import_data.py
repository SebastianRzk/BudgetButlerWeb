from datetime import datetime
from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.core.file_system import write_import
from butler_offline.core.export.json_to_text_mapper import JSONToTextMapper
from butler_offline.viewcore.context import generate_transactional_context
from butler_offline.viewcore.converter import datum_to_string
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.base_html import set_success_message, set_error_message
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.core import configuration_provider
from butler_offline.online_services.butler_online.session import get_partnername, login
from butler_offline.online_services.butler_online.einzelbuchungen import get_einzelbuchungen, delete_einzelbuchungen
from butler_offline.online_services.butler_online.gemeinsame_buchungen import get_gemeinsame_buchungen, \
    upload_gemeinsame_buchungen, delete_gemeinsame_buchungen
from butler_offline.online_services.butler_online.settings import set_kategorien
from butler_offline.core.export.json_report import JSONReport
from butler_offline.core.export.text_report import TextReportWriter, TextReportReader
import logging


def _mapping_passt(post_parameter, unpassende_kategorien):
    for unpassenden_kategorie in unpassende_kategorien:
        if not str(unpassenden_kategorie) + "_mapping" in post_parameter:
            return False
    return True


def _import(import_data, gemeinsam):
    logging.info('importing data:')
    logging.info(str(import_data))
    if gemeinsam :
        database_instance().gemeinsamebuchungen.parse(import_data)
        database_instance().gemeinsamebuchungen.taint()
    else:
        database_instance().einzelbuchungen.parse(import_data)
        database_instance().einzelbuchungen.taint()


def _map_kategorien(import_data, unpassende_kategorien, post_parameter):
    logging.info('Mappe Kategorien %s -> %s', unpassende_kategorien, post_parameter)

    for unpassende_kategorie in unpassende_kategorien:
        mapping_string = post_parameter[str(unpassende_kategorie) + '_mapping']
        if mapping_string == 'neue Kategorie anlegen':
            logging.info(unpassende_kategorie + ' muss nicht gemappt werden')
            continue
        mapping_kategorie = mapping_string[4:len(' importieren') * -1]
        logging.info('%s wird in %s gemappt', unpassende_kategorie,  mapping_kategorie)
        import_data.Kategorie = import_data.Kategorie.map(lambda x: _kategorien_map(x, unpassende_kategorie, mapping_kategorie))
    return import_data


def index(request):
    return request_handler.handle_request(request, handle_request , 'shared/import.html')


def _get_success_message(last_elements):
    number = len(last_elements)
    if number == 1:
        return '1 Buchung wurde importiert'
    return '{anzahl} Buchungen wurden importiert'.format(anzahl=number)


def handle_request(request, import_prefix='', gemeinsam=False):
    context = generate_transactional_context('import')
    if request.method == "POST":
        if post_action_is(request, 'load_online_transactions'):
            serverurl = request.values['server']
            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])

            auth_container = login(serverurl, request.values['email'], request.values['password'])

            json_report = get_einzelbuchungen(serverurl, auth_container)
            logging.info(str(json_report))
            logging.info('Mapping to text report')
            text_report = JSONToTextMapper().map(json_report)
            logging.info(str(text_report))

            response = handle_request(PostRequest({'import': text_report}), import_prefix='Internet')

            delete_einzelbuchungen(serverurl, auth_container=auth_container)
            return response

        if post_action_is(request, 'load_online_gemeinsame_transactions'):
            serverurl = request.values['server']
            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])
            logging.info(serverurl)
            auth_container = login(serverurl, request.values['email'], request.values['password'])
            online_username = auth_container.online_name()
            logging.info('butler_online username: %s', online_username)

            online_content = get_gemeinsame_buchungen(serverurl, auth_container)
            logging.info(str(online_content))
            table = JSONReport().dataframe_from_json_gemeinsam(online_content)

            logging.info('table before person mapping %s', table)
            table.Person = table.Person.map(lambda x: database_instance().name if x == online_username else configuration_provider.get_configuration('PARTNERNAME'))
            online_content = TextReportWriter().generate_report(table)
            response = handle_request(PostRequest({'import': online_content}), import_prefix='Internet_Gemeinsam', gemeinsam=True)

            delete_gemeinsame_buchungen(serverurl, auth_container=auth_container)
            return response

        elif post_action_is(request, 'set_kategorien'):
            kategorien = ','.join(sorted(database_instance().einzelbuchungen.get_alle_kategorien(hide_ausgeschlossene_kategorien=True)))
            serverurl = request.values['server']

            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])

            auth_container = login(serverurl, request.values['email'], request.values['password'])
            set_kategorien(serverurl, kategorien=kategorien, auth_container=auth_container)
            set_success_message(context, 'Kategorien erfolgreich in die Online-Version übertragen.')

        elif post_action_is(request, 'upload_gemeinsame_transactions'):
            serverurl = request.values['server']
            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])
            logging.info(serverurl)
            auth_container = login(serverurl, request.values['email'], request.values['password'])
            online_username = auth_container.online_name()
            logging.info('butler_online username: %s', online_username)
            offline_username = database_instance().name
            logging.info('butler offline username: %s', offline_username)
            online_partnername = get_partnername(serverurl, auth_container=auth_container)
            logging.info('butler online partnername: %s', online_partnername)
            offline_partnername = configuration_provider.get_configuration('PARTNERNAME')
            logging.info('butler offline partnername: %s', offline_partnername)

            buchungen = database_instance().gemeinsamebuchungen.get_renamed_list(offline_username,
                                                                                 online_username,
                                                                                 offline_partnername,
                                                                                 online_partnername)
            request_data = []

            for buchung in buchungen:
                request_data.append(
                    {
                        'datum': datum_to_string(buchung['Datum']),
                        'name': buchung['Name'],
                        'wert': buchung['Wert'],
                        'kategorie': buchung['Kategorie'],
                        'zielperson': buchung['Person']
                    }
                )
            anzahl_buchungen = len(buchungen)
            result = upload_gemeinsame_buchungen(serverurl, request_data, auth_container)
            if result:
                set_success_message(context, '{anzahl_buchungen} Buchungen wurden erfolgreich hochgeladen.'.format(anzahl_buchungen=anzahl_buchungen))
                database_instance().gemeinsamebuchungen.drop_all()
            else:
                set_error_message(context, 'Fehler beim Hochladen der gemeinsamen Buchungen.')

        else:
            logging.debug(str(request.values))
            content = request.values['import'].replace('\r', '')
            write_import(import_prefix + 'Import_' + str(datetime.now()), content)

            imported_values = TextReportReader().read(content)
            datenbank_kategorien = set(
                database_instance().einzelbuchungen.get_alle_kategorien())
            nicht_passende_kategorien = []
            for imported_kategorie in set(imported_values.Kategorie):
                if imported_kategorie not in datenbank_kategorien:
                    nicht_passende_kategorien.append(imported_kategorie)

            if 'Person' in imported_values.columns:
                gemeinsam = True

            if not nicht_passende_kategorien:
                logging.info('keine unpassenden kategorien gefunden')
                logging.info('beginne mit dem direkten import')
                _import(imported_values, gemeinsam)

                last_elements = []
                for row_index, row in imported_values.iterrows():
                    last_elements.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))
                context['ausgaben'] = last_elements
                context = set_success_message(context, _get_success_message(last_elements))
            elif _mapping_passt(request.values, nicht_passende_kategorien):
                logging.info('import kann durchgeführt werden, weil mapping vorhanden')
                imported_values = _map_kategorien(imported_values, nicht_passende_kategorien, request.values)
                _import(imported_values, gemeinsam)

                last_elements = []
                for row_index, row in imported_values.iterrows():
                    last_elements.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))
                context['ausgaben'] = last_elements
                context = set_success_message(context, _get_success_message(last_elements))
            else:
                logging.info("Nicht passende Kategorien: %s", nicht_passende_kategorien)
                options = ['neue Kategorie anlegen']
                for kategorie_option in datenbank_kategorien:
                    options.append('als ' + str(kategorie_option) + ' importieren')
                options = sorted(options)
                options.insert(0, 'neue Kategorie anlegen')
                context['element_titel'] = 'Kategorien zuweisen'
                context['unpassende_kategorien'] = nicht_passende_kategorien
                context['optionen'] = options
                context['import'] = request.values['import']
                context['special_page'] = 'shared/import_mapping.html'

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
