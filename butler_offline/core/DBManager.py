'''
Read panda files
'''

from _io import StringIO

from butler_offline.core import file_system
from butler_offline.core.database import Database
import pandas as pd

KEYWORD_EINZELBUCHUNGEN = 'Einzelbuchungen'
KEYWORD_DAUERAUFRTAEGE = 'Dauerauftraege'
KEYWORD_GEMEINSAME_BUCHUNGEN = 'Gemeinsame Buchungen'
KEYWORD_SPARBUCHUNGEN = 'Sparbuchungen'

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
    print('READER: Einzelbuchungen gelesen')

    database.dauerauftraege.parse(_to_table(parser.dauerauftraege()))
    print('READER: Daueraufträge gelesen')

    database.gemeinsamebuchungen.parse(_to_table(parser.gemeinsame_buchungen()))
    print('READER: Gemeinsame Buchungen gelesen')

    if parser.sparbuchungen():
        database.sparbuchungen.parse(_to_table(parser.sparbuchungen()))
        print('READER: Sparbuchungen gelesen')

    print('READER: Refreshe Database')
    database.refresh()
    print('READER: Refresh done')
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

    file_system.instance().write(database_path_from(database.name), content)
    print("WRITER: All Saved")



def database_path_from(username):
    return '../Database_' + username + '.csv'


class DatabaseParser:
    def __init__(self):
        self._reader = MultiPartCsvReader(
            set([KEYWORD_EINZELBUCHUNGEN, KEYWORD_DAUERAUFRTAEGE, KEYWORD_GEMEINSAME_BUCHUNGEN, KEYWORD_SPARBUCHUNGEN]),
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
