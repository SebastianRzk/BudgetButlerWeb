from _io import StringIO
from butler_offline.core import file_system
from butler_offline.core.database import Database
from butler_offline.core.configuration_provider import configuration_provider
import pandas as pd
import logging

KEYWORD_EINZELBUCHUNGEN = 'Einzelbuchungen'
KEYWORD_DAUERAUFRTAEGE = 'Dauerauftraege'
KEYWORD_GEMEINSAME_BUCHUNGEN = 'Gemeinsame Buchungen'
KEYWORD_SPARBUCHUNGEN = 'Sparbuchungen'
KEYWORD_SPARKONTOS = 'Sparkontos'
KEYWORD_DEPOTWERTE = 'Depotwerte'
KEYWORD_ORDER = 'Order'
KEYWORD_ORDERDAUERAUFTRAG = 'Dauerauftr_Ordr'
KEYWORD_DEPOTAUSZUEGE = 'Depotauszuege'

KEYWORD_LINEBREAK = '\n'


def _to_table(content):
    return pd.read_csv(StringIO(content))


def read(nutzername, ausgeschlossene_kategorien):
    if not file_system.instance().read(database_path_from(nutzername)):
        neue_datenbank = Database(nutzername)
        write(neue_datenbank)

    file_content = file_system.instance().read(database_path_from(nutzername))

    parser = DatabaseParser()
    parser.from_string(file_content)

    database = Database(nutzername, ausgeschlossene_kategorien=ausgeschlossene_kategorien)

    database.einzelbuchungen.parse(_to_table(parser.einzelbuchungen()))
    logging.info('READER: Einzelbuchungen gelesen')

    database.dauerauftraege.parse(_to_table(parser.dauerauftraege()))
    logging.info('READER: Daueraufträge gelesen')

    database.gemeinsamebuchungen.parse(_to_table(parser.gemeinsame_buchungen()))
    logging.info('READER: Gemeinsame Buchungen gelesen')

    if parser.sparkontos():
        database.sparkontos.parse(_to_table(parser.sparkontos()))
        logging.info('READER: Sparkontos gelesen')

    if parser.sparbuchungen():
        database.sparbuchungen.parse(_to_table(parser.sparbuchungen()))
        logging.info('READER: Sparbuchungen gelesen')

    if parser.depotwerte():
        database.depotwerte.parse_and_migrate(_to_table(parser.depotwerte()))
        logging.info('READER: Depotwerte gelesen')

    if parser.order():
        database.order.parse(_to_table(parser.order()))
        logging.info('READER: Depotwerte gelesen')

    if parser.depotauszuege():
        database.depotauszuege.parse(_to_table(parser.depotauszuege()))
        logging.info('READER: Depotauszuege gelesen')

    if parser.order_dauerauftrag():
        database.orderdauerauftrag.parse(_to_table(parser.order_dauerauftrag()))
        logging.info('READER: Order Dauerauftrag gelesen')

    logging.info('READER: Refreshe Database')
    database.refresh()
    logging.info('READER: Refresh done')
    return database


def wrap_tableheader(table_header_name):
    return '{} {} {}'.format(KEYWORD_LINEBREAK, table_header_name, KEYWORD_LINEBREAK)


def write(database):

    content = database.einzelbuchungen.get_static_content().to_csv(index=False)

    content += wrap_tableheader(KEYWORD_DAUERAUFRTAEGE)
    content += database.dauerauftraege.content.to_csv(index=False)

    content += wrap_tableheader(KEYWORD_GEMEINSAME_BUCHUNGEN)
    content += database.gemeinsamebuchungen.content.to_csv(index=False)

    content += wrap_tableheader(KEYWORD_SPARBUCHUNGEN)
    content += database.sparbuchungen.get_static_content().to_csv(index=False)

    content += wrap_tableheader(KEYWORD_SPARKONTOS)
    content += database.sparkontos.get_static_content().to_csv(index=False)

    content += wrap_tableheader(KEYWORD_DEPOTWERTE)
    content += database.depotwerte.get_static_content().to_csv(index=False)

    content += wrap_tableheader(KEYWORD_ORDER)
    content += database.order.get_static_content().to_csv(index=False)

    content += wrap_tableheader(KEYWORD_ORDERDAUERAUFTRAG)
    content += database.orderdauerauftrag.get_static_content().to_csv(index=False)

    content += wrap_tableheader(KEYWORD_DEPOTAUSZUEGE)
    content += database.depotauszuege.get_static_content().to_csv(index=False)

    file_system.instance().write(database_path_from(database.name), content)
    print("WRITER: All Saved")



def database_path_from(username):
    return configuration_provider.get_database_path() + '/Database_' + username + '.csv'


class DatabaseParser:
    def __init__(self):
        self._reader = MultiPartCsvReader(
            set([
                KEYWORD_EINZELBUCHUNGEN,
                KEYWORD_DAUERAUFRTAEGE,
                KEYWORD_GEMEINSAME_BUCHUNGEN,
                KEYWORD_SPARBUCHUNGEN,
                KEYWORD_SPARKONTOS,
                KEYWORD_DEPOTWERTE,
                KEYWORD_ORDER,
                KEYWORD_DEPOTAUSZUEGE,
                KEYWORD_ORDERDAUERAUFTRAG
            ]),
            start_token=KEYWORD_EINZELBUCHUNGEN)

    def from_string(self, lines):
        self._reader.from_string(lines)

    def einzelbuchungen(self):
        return self._reader.get_string(KEYWORD_EINZELBUCHUNGEN)

    def dauerauftraege(self):
        return self._reader.get_string(KEYWORD_DAUERAUFRTAEGE)

    def gemeinsame_buchungen(self):
        return self._reader.get_string(KEYWORD_GEMEINSAME_BUCHUNGEN)

    def sparbuchungen(self):
        return self._reader.get_string(KEYWORD_SPARBUCHUNGEN)

    def sparkontos(self):
        return self._reader.get_string(KEYWORD_SPARKONTOS)

    def depotwerte(self):
        return self._reader.get_string(KEYWORD_DEPOTWERTE)

    def order(self):
        return self._reader.get_string(KEYWORD_ORDER)

    def depotauszuege(self):
        return self._reader.get_string(KEYWORD_DEPOTAUSZUEGE)

    def order_dauerauftrag(self):
        return self._reader.get_string(KEYWORD_ORDERDAUERAUFTRAG)


class MultiPartCsvReader:
    def __init__(self, token, start_token):
        self._token = token
        self._start_token = start_token
        self._tables = {}

    def from_string(self, lines):
        self._tables = dict.fromkeys(self._token, '')
        mode = self._start_token

        for line in lines:
            line = line.strip()
            if line == '':
                continue

            if line in self._token:
                mode = line
                continue

            if not ',' in line:
                break

            self._tables[mode] = self._tables[mode] + KEYWORD_LINEBREAK + line

    def get_string(self, token):
        return self._tables[token].strip()
