'''
Created on 10.05.2017

@author: sebastian
'''

from datetime import date, timedelta
import os
import sys
import unittest
from pandas.core.frame import DataFrame
from core.DatabaseModule import Database
from test import DBManagerStub

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../')

import core.DatabaseModule as db
from viewcore.converter import datum, laenge
from viewcore import viewcore
from viewcore import configuration_provider


class abrechnen(unittest.TestCase):
    abrechnung = """Abrechnung vom 01.01.2010
########################################
 Ergebnis:
test muss an Maureen noch 5.00€ überweisen.

Ausgaben von Maureen           -10.00
Ausgaben von test                0.00
--------------------------------------
Gesamt                         -10.00
 
 
########################################
 Gesamtausgaben pro Person 
########################################
 Datum      Kategorie    Name                    Wert
17.03.2017  some kategorie some name              -5.00


########################################
 Ausgaben von Maureen
########################################
 Datum      Kategorie    Name                    Wert
17.03.2017  some kategorie some name             -10.00


########################################
 Ausgaben von test
########################################
 Datum      Kategorie    Name                    Wert


#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-17,some kategorie,some name,-5.00,False
#######MaschinenimportEnd
"""


    def set_up(self):
        DBManagerStub.setup_db_for_test()
        DBManagerStub.stub_abrechnungs_write()
        configuration_provider.stub_me('''
            PARTNERNAME:Maureen
            ''')


    def test_abrechnen_shouldAddEinzelbuchungen(self):
        self.set_up()
        db = viewcore.database_instance()
        db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', 10, viewcore.name_of_partner())
        db.abrechnen()

        assert len(db.einzelbuchungen.content) == 1
        uebertragene_buchung = db.einzelbuchungen.get(0)
        assert uebertragene_buchung['Name'] == 'some name'
        assert uebertragene_buchung['Datum'] == datum('17.03.2017')
        assert uebertragene_buchung['Kategorie'] == 'some kategorie'
        assert uebertragene_buchung['Wert'] == '5.00'

    def test_abrechnen_shouldPrintFileContent(self):
        self.set_up()
        db = viewcore.database_instance()
        db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -10, viewcore.name_of_partner())
        viewcore.stub_today_with(datum('01.01.2010'))
        abrechnungs_text = db.abrechnen()
        viewcore.reset_viewcore_stubs()

        assert abrechnungs_text == self.abrechnung
class converter_test(unittest.TestCase):
    def test_frame_to_list_of_dicts_withEmptyDataframe_shouldReturnEmptyList(self):
        empty_dataframe = DataFrame()

        result = db.Database('test_database').frame_to_list_of_dicts(empty_dataframe)

        assert result == []

    def test_frame_to_list_of_dicts_withDataframe_shouldReturnListOfDicts(self):
        dataframe = DataFrame([{'col1':'test1', 'col2': 1}, {'col1':'test2', 'col2': 2}])

        result = db.Database('test_database').frame_to_list_of_dicts(dataframe)

        print(result)
        assert len(result) == 2
        assert result[0]['col1'] == 'test1'
        assert result[0]['col2'] == 1
        assert result[1]['col1'] == 'test2'
        assert result[1]['col2'] == 2


class refresh(unittest.TestCase):
    def teste_refresh_with_empty_database(self):
        component_under_test = db.Database('test_database')
        component_under_test.refresh()

    def teste_refresh_shouldAddEinzelbuchungenVonDauerauftrag(self):
        component_under_test = db.Database('test_database')
        component_under_test.dauerauftraege.add(datum('10.01.2010'), datum('11.03.2010'), '', '', 'monatlich', 20)
        component_under_test.refresh()

        assert len(component_under_test.einzelbuchungen.content) == 3

