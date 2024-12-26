import logging
from _io import StringIO

import pandas as pd

from file_system import FileSystemImpl

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


def read(database_path: str):
    file_content = FileSystemImpl().read(database_path)

    parser = DatabaseParser()
    parser.from_string(file_content)

    einzelbuchungen = _to_table(parser.einzelbuchungen())
    logging.info('READER: Einzelbuchungen gelesen')
    einzelbuchungen['Name'] = einzelbuchungen['Name'].map(lambda name: name.replace(',', '').replace('"', ''))
    einzelbuchungen = einzelbuchungen[['Datum', 'Kategorie', 'Name', 'Wert']]
    logging.info('READER: Einzelbuchungen migriert')

    dauerauftraege = _to_table(parser.dauerauftraege())
    logging.info('READER: Daueraufträge gelesen')
    dauerauftraege['Rhythmus'] = dauerauftraege['Rhythmus'].map(map_rhythmus)
    dauerauftraege = dauerauftraege[['Startdatum', 'Endedatum', 'Kategorie', 'Name', 'Rhythmus', 'Wert']]
    logging.info('READER: Daueraufträge migriert')

    gemeinsamebuchungen = _to_table(parser.gemeinsame_buchungen())
    logging.info('READER: Gemeinsame Buchungen gelesen')
    gemeinsamebuchungen = gemeinsamebuchungen[['Datum', 'Kategorie', 'Name', 'Wert', 'Person']]
    logging.info('READER: Gemeinsame Buchungen migriert')

    sparkontos = _to_table(parser.sparkontos())
    logging.info('READER: Sparkontos gelesen')
    sparkontos = sparkontos[['Kontoname', 'Kontotyp']]
    logging.info('READER: Sparkontos migriert')

    sparbuchungen = _to_table(parser.sparbuchungen())
    logging.info('READER: Sparbuchungen gelesen')
    sparbuchungen['Typ'] = sparbuchungen.apply(lambda df: migriere_sparbuchung_typ(df['Wert'], df['Typ']), axis=1)
    sparbuchungen['Wert'] = sparbuchungen['Wert'].abs()
    sparbuchungen = sparbuchungen[['Datum', 'Name', 'Wert', 'Typ', 'Konto']]
    logging.info('READER: Sparbuchungen migriert')

    depotwerte = _to_table(parser.depotwerte())
    logging.info('READER: Depotwerte gelesen')
    depotwerte = depotwerte[['Name', 'ISIN', 'Typ']]
    logging.info('READER: Depotwerte migriert')

    order = _to_table(parser.order())
    logging.info('READER: Depotwerte gelesen')
    order['Typ'] = order['Wert'].apply(migriere_order_typ)
    order['Wert'] = order['Wert'].abs()
    order = order[['Datum', 'Name', 'Konto', 'Depotwert', 'Wert', 'Typ']]
    logging.info('READER: Depotwerte migriert')

    depotauszuege = _to_table(parser.depotauszuege())
    logging.info('READER: Depotauszuege gelesen')
    depotauszuege = depotauszuege[['Datum', 'Depotwert', 'Konto', 'Wert']]
    logging.info('READER: Depotauszuege migriert')

    orderdauerauftrag = _to_table(parser.order_dauerauftrag())
    logging.info('READER: Order Dauerauftrag gelesen')
    orderdauerauftrag['Rhythmus'] = orderdauerauftrag['Rhythmus'].map(map_rhythmus)
    orderdauerauftrag['Typ'] = orderdauerauftrag['Wert'].apply(migriere_order_typ)
    orderdauerauftrag['Wert'] = orderdauerauftrag['Wert'].abs()
    orderdauerauftrag = orderdauerauftrag[
        ['Startdatum', 'Endedatum', 'Rhythmus', 'Name', 'Konto', 'Depotwert', 'Wert', 'Typ']]

    logging.info('READER: Order Dauerauftrag migriert')

    content = wrap_tableheader("Datum,Kategorie,Name,Wert")
    content += einzelbuchungen.to_csv(index=False)
    content += wrap_tableheader(KEYWORD_DAUERAUFRTAEGE)
    content += dauerauftraege.to_csv(index=False)
    content += wrap_tableheader(KEYWORD_GEMEINSAME_BUCHUNGEN)
    content += gemeinsamebuchungen.to_csv(index=False)
    content += wrap_tableheader(KEYWORD_SPARBUCHUNGEN)
    content += sparbuchungen.to_csv(index=False)
    content += wrap_tableheader(KEYWORD_SPARKONTOS)
    content += sparkontos.to_csv(index=False)
    content += wrap_tableheader(KEYWORD_DEPOTWERTE)
    content += depotwerte.to_csv(index=False)
    content += wrap_tableheader(KEYWORD_ORDER)
    content += order.to_csv(index=False)
    content += wrap_tableheader(KEYWORD_ORDERDAUERAUFTRAG)
    content += orderdauerauftrag.to_csv(index=False)
    content += wrap_tableheader(KEYWORD_DEPOTAUSZUEGE)
    content += depotauszuege.to_csv(index=False)
    return content


def migriere_sparbuchung_typ(wert, typ):
    if typ != 'Manueller Auftrag':
        return typ
    if wert < 0:
        return 'Manuelle Auszahlung'
    return 'Manuelle Einzahlung'


def migriere_order_typ(wert):
    if wert < 0:
        return 'Verkauf'
    return 'Kauf'

def map_rhythmus (rhythmus):
    if rhythmus == 'jaehrlich':
        return 'jährlich'
    if rhythmus == 'vierteljaehrlich':
        return 'vierteljährlich'
    if rhythmus == 'halbjaehrlich':
        return 'halbjährlich'
    return rhythmus

def wrap_tableheader(table_header_name):
    return '{} {} {}'.format(KEYWORD_LINEBREAK, table_header_name, KEYWORD_LINEBREAK)

class DatabaseParser:
    def __init__(self):
        self._reader = MultiPartCsvReader(
            {
                KEYWORD_EINZELBUCHUNGEN,
                KEYWORD_DAUERAUFRTAEGE,
                KEYWORD_GEMEINSAME_BUCHUNGEN,
                KEYWORD_SPARBUCHUNGEN,
                KEYWORD_SPARKONTOS,
                KEYWORD_DEPOTWERTE,
                KEYWORD_ORDER,
                KEYWORD_DEPOTAUSZUEGE,
                KEYWORD_ORDERDAUERAUFTRAG
            },
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
