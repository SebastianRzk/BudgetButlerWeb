from datetime import datetime
from butler_offline.core.file_system import write_import
from butler_offline.core.export.json_to_text_mapper import JSONToTextMapper
from butler_offline.viewcore.converter import datum_to_string
from butler_offline.viewcore import request_handler
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
from butler_offline.viewcore.converter import datetime_to_filesystem_string
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.viewcore.context.builder import generate_transactional_page_context
from butler_offline.core import file_system


class ImportDataContext:
    def __init__(self,
                 name: str,
                 einzelbuchungen: Einzelbuchungen,
                 gemeinsamebuchungen: Gemeinsamebuchungen,
                 filesystem: file_system.FileSystemImpl
                 ):
        self._name = name
        self._einzelbuchungen = einzelbuchungen
        self._gemeinsamebuchungen = gemeinsamebuchungen
        self._filesystem = filesystem

    def name(self) -> str:
        return self._name

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen

    def gemeinsamebuchungen(self) -> Gemeinsamebuchungen:
        return self._gemeinsamebuchungen

    def filesystem(self) -> file_system.FileSystemImpl:
        return self._filesystem


def _mapping_passt(post_parameter, unpassende_kategorien):
    for unpassenden_kategorie in unpassende_kategorien:
        if not str(unpassenden_kategorie) + "_mapping" in post_parameter:
            return False
    return True


def _import(import_data, gemeinsam, context: ImportDataContext):
    logging.info('importing data:')
    logging.info(str(import_data))
    if gemeinsam:
        context.gemeinsamebuchungen().parse(import_data)
        context.gemeinsamebuchungen().taint()
    else:
        context.einzelbuchungen().parse(import_data)
        context.einzelbuchungen().taint()


def _map_kategorien(import_data, unpassende_kategorien, post_parameter):
    logging.info('Mappe Kategorien %s -> %s', unpassende_kategorien, post_parameter)

    for unpassende_kategorie in unpassende_kategorien:
        mapping_string = post_parameter[str(unpassende_kategorie) + '_mapping']
        if mapping_string == 'neue Kategorie anlegen':
            logging.info(unpassende_kategorie + ' muss nicht gemappt werden')
            continue
        mapping_kategorie = mapping_string[4:len(' importieren') * -1]
        logging.info('%s wird in %s gemappt', unpassende_kategorie, mapping_kategorie)
        import_data.Kategorie = import_data.Kategorie.map(
            lambda x: _kategorien_map(x, unpassende_kategorie, mapping_kategorie))
    return import_data


def _get_success_message(last_elements):
    number = len(last_elements)
    if number == 1:
        return '1 Buchung wurde importiert'
    return '{anzahl} Buchungen wurden importiert'.format(anzahl=number)


def handle_request(request, context: ImportDataContext):
    return handle_request_internally(request=request, context=context)


def handle_request_internally(request, context: ImportDataContext, import_prefix='', gemeinsam=False):
    result_context = generate_transactional_page_context('import')
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

            response = handle_request_internally(
                request=PostRequest({'import': text_report}),
                import_prefix='Internet',
                context=context
            )

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
            table.Person = table.Person.map(
                lambda x: context.name() if x == online_username else configuration_provider.get_configuration(
                    'PARTNERNAME'))
            online_content = TextReportWriter().generate_report(table)
            response = handle_request_internally(
                request=PostRequest({'import': online_content}),
                import_prefix='Internet_Gemeinsam',
                gemeinsam=True,
                context=context
            )

            delete_gemeinsame_buchungen(serverurl, auth_container=auth_container)
            return response

        elif post_action_is(request, 'set_kategorien'):
            kategorien = ','.join(
                sorted(context.einzelbuchungen().get_alle_kategorien(hide_ausgeschlossene_kategorien=True)))
            serverurl = request.values['server']

            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])

            auth_container = login(serverurl, request.values['email'], request.values['password'])
            set_kategorien(serverurl, kategorien=kategorien, auth_container=auth_container)
            result_context.add_user_success_message('Kategorien erfolgreich in die Online-Version übertragen.')

        elif post_action_is(request, 'upload_gemeinsame_transactions'):
            serverurl = request.values['server']
            serverurl = _add_protokoll_if_needed(serverurl)
            _save_server_creds(serverurl, request.values['email'])
            logging.info(serverurl)
            auth_container = login(serverurl, request.values['email'], request.values['password'])
            online_username = auth_container.online_name()
            logging.info('butler_online username: %s', online_username)
            offline_username = context.name()
            logging.info('butler offline username: %s', offline_username)
            online_partnername = get_partnername(serverurl, auth_container=auth_container)
            logging.info('butler online partnername: %s', online_partnername)
            offline_partnername = configuration_provider.get_configuration('PARTNERNAME')
            logging.info('butler offline partnername: %s', offline_partnername)

            buchungen = context.gemeinsamebuchungen().get_renamed_list(offline_username,
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
                result_context.add_user_success_message(
                    '{anzahl_buchungen} Buchungen wurden erfolgreich hochgeladen.'.format(
                        anzahl_buchungen=anzahl_buchungen))
                context.gemeinsamebuchungen().drop_all()
            else:
                result_context.add_user_error_message('Fehler beim Hochladen der gemeinsamen Buchungen.')

        else:
            logging.debug(str(request.values))
            content = request.values['import'].replace('\r', '')
            write_import(
                file_name=import_prefix + 'Import_' + datetime_to_filesystem_string(datetime.now()),
                file_content=content,
                filesystem=context.filesystem())

            imported_values = TextReportReader().read(content)
            datenbank_kategorien = set(context.einzelbuchungen().get_alle_kategorien())
            nicht_passende_kategorien = []
            for imported_kategorie in set(imported_values.Kategorie):
                if imported_kategorie not in datenbank_kategorien:
                    nicht_passende_kategorien.append(imported_kategorie)

            if 'Person' in imported_values.columns:
                gemeinsam = True

            if not nicht_passende_kategorien:
                logging.info('keine unpassenden kategorien gefunden')
                logging.info('beginne mit dem direkten import')
                _import(
                    imported_values,
                    gemeinsam,
                    context=context)

                last_elements = []
                for row_index, row in imported_values.iterrows():
                    last_elements.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))
                result_context.add('ausgaben', last_elements)
                result_context.add_user_success_message(_get_success_message(last_elements))
            elif _mapping_passt(request.values, nicht_passende_kategorien):
                logging.info('import kann durchgeführt werden, weil mapping vorhanden')
                imported_values = _map_kategorien(imported_values, nicht_passende_kategorien, request.values)
                _import(
                    imported_values,
                    gemeinsam,
                    context=context
                )

                last_elements = []
                for row_index, row in imported_values.iterrows():
                    last_elements.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))
                result_context.add('ausgaben', last_elements)
                result_context.add_user_success_message(_get_success_message(last_elements))
            else:
                logging.info("Nicht passende Kategorien: %s", nicht_passende_kategorien)
                options = ['neue Kategorie anlegen']
                for kategorie_option in datenbank_kategorien:
                    options.append('als ' + str(kategorie_option) + ' importieren')
                options = sorted(options)
                options.insert(0, 'neue Kategorie anlegen')
                result_context.add('element_titel', 'Kategorien zuweisen')
                result_context.add('unpassende_kategorien', nicht_passende_kategorien)
                result_context.add('optionen', options)
                result_context.add('import', request.values['import'])
                result_context.add('special_page', 'shared/import_mapping.html')

    result_context.add('ONLINE_DEFAULT_SERVER', configuration_provider.get_configuration('ONLINE_DEFAULT_SERVER'))
    result_context.add('ONLINE_DEFAULT_USER', configuration_provider.get_configuration('ONLINE_DEFAULT_USER'))
    return result_context


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


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='shared/import.html',
        context_creator=lambda db: ImportDataContext(
            gemeinsamebuchungen=db.gemeinsamebuchungen,
            einzelbuchungen=db.einzelbuchungen,
            name=db.name,
            filesystem=file_system.instance()
        )
    )
