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

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../')

import core.DatabaseModule as db
from viewcore.converter import datum, laenge
from viewcore.converter import time


def _zero():
    return timedelta(minutes=0)

class stechzeiten(unittest.TestCase):

    def teste_add(self):
        component_under_test = db.Database('test_database')

        component_under_test.add_stechzeit(date.today(), time('0:0'), time('1:23'), 'Datev')

        assert len(component_under_test.stechzeiten) == 1
        assert component_under_test.stechzeiten.Datum[0] == date.today()
        assert component_under_test.stechzeiten.Einstechen[0] == time('0:0')
        assert component_under_test.stechzeiten.Ausstechen[0] == time('1:23')
        assert component_under_test.stechzeiten.Arbeitgeber[0] == 'Datev'

    def teste_stechzeitenVorhanden_withNoExistingStechzeit_shouldReturnFalse(self):
        component_under_test = db.Database('test_database')
        assert not component_under_test.stechzeiten_vorhanden()

    def teste_stechzeitenVorhanden_withOneExisitingStechzeit_shouldReturnTrue(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_stechzeit(date.today(), time('2:3'), time('6:32'), 'BlaBla')

        assert component_under_test.stechzeiten_vorhanden()



    def teste_edit(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_stechzeit(date.today(), time('2:3'), time('6:32'), 'BlaBla')

        component_under_test.edit_stechzeit(0, date.today(), time('0:0'), time('1:23'), 'Datev')


        assert len(component_under_test.stechzeiten) == 1
        assert component_under_test.stechzeiten.Datum[0] == date.today()
        assert component_under_test.stechzeiten.Einstechen[0] == time('0:0')
        assert component_under_test.stechzeiten.Ausstechen[0] == time('1:23')
        assert component_under_test.stechzeiten.Arbeitgeber[0] == 'Datev'


    def test_withOnlyOneStechzeit_shouldReturnWeekOfTodayWithTimdelta(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_stechzeit(date.today(), time('0:0'), time('1:23'), 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        assert len(result.keys()) == 1
        assert result.keys() == set([date.today().isocalendar()[1]])
        assert result[date.today().isocalendar()[1]] == (timedelta(hours=1, minutes=23), _zero())

    def test_withTwoStechzeitInSameWeek_shouldReturnCummulatedResult(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_stechzeit(date.today(), time('0:0'), time('1:23'), 'Datev')
        component_under_test.add_stechzeit(date.today(), time('0:0'), time('1:23'), 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        assert len(result.keys()) == 1
        assert result.keys() == set([date.today().isocalendar()[1]])
        assert result[date.today().isocalendar()[1]] == (timedelta(hours=2, minutes=46), _zero())

    def test_withTwoStechzeitInDifferendWeeks_shouldReturnTwoResults(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_stechzeit(date.today(), time('0:0'), time('1:23'), 'Datev')
        component_under_test.add_stechzeit(date.today() - timedelta(days=7), time('0:0'), time('1:23'), 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        assert len(result.keys()) == 2
        assert result.keys() == set([date.today().isocalendar()[1], date.today().isocalendar()[1] - 1])
        assert result[date.today().isocalendar()[1]] == (timedelta(hours=1, minutes=23), _zero())
        assert result[date.today().isocalendar()[1] - 1] == (timedelta(hours=1, minutes=23), _zero())

    def test_sollzeitOfFirtstWeekday_shouldReturnWeekOfTodayWithSollzeit(self):
        component_under_test = db.Database('test_database')

        component_under_test.add_soll_zeit(datum('29/05/2017'), datum('29/05/2017'), time('1:02'), 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(datum('29/05/2017').year)

        assert datum('29/05/2017').isocalendar()[1] in result
        assert result[datum('29/05/2017').isocalendar()[1]] == (_zero(), timedelta(hours=1, minutes=2))

    def test_sollzeitOfLastWeekday_shouldReturnWeekOfTodayWithSollzeit(self):
        component_under_test = db.Database('test_database')

        component_under_test.add_soll_zeit(datum('02/06/2017'), datum('02/06/2017'), time('1:02'), 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(datum('02/06/2017').year)

        assert datum('02/06/2017').isocalendar()[1] in result
        assert result[datum('02/06/2017').isocalendar()[1]] == (_zero(), timedelta(hours=1, minutes=2))

    def test_withTwoSollzeiten_shouldReturnCummulatedResults(self):
        component_under_test = db.Database('test_database')

        component_under_test.add_soll_zeit(datum('16/5/2017'), datum('16/5/2017'), time('1:02'), 'Datev')
        component_under_test.add_soll_zeit(datum('15/5/2017'), datum('15/5/2017'), time('0:30'), 'Datev')

        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        print(result)
        assert datum('16/5/2017').isocalendar()[1] in result.keys()
        assert result[datum('16/5/2017').isocalendar()[1]] == (_zero(), timedelta(hours=1, minutes=32))

    def test_withTwoSollzeitenSameDate_shouldReturnCummulatedResults(self):
        component_under_test = db.Database('test_database')

        component_under_test.add_soll_zeit(datum('01/06/2017'), datum('01/06/2017'), time('1:02'), 'Datev')
        component_under_test.add_soll_zeit(datum('01/06/2017'), datum('01/06/2017'), time('0:30'), 'Datev')

        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        assert datum('01/06/2017').isocalendar()[1] in result
        assert result[datum('01/06/2017').isocalendar()[1]] == (_zero(), timedelta(hours=1, minutes=32))

    def test_withWochenSollzeit_shouldIgnoreWochenende(self):
        component_under_test = db.Database('test_database')

        component_under_test.add_soll_zeit(datum('15/5/2017'), datum('21/5/2017'), time('1:02'), 'Datev')

        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        assert datum('15/5/2017').isocalendar()[1] in result.keys()
        assert result[datum('15/5/2017').isocalendar()[1]] == (_zero(), timedelta(hours=5, minutes=10))


    def test_anzahlStechzeiten_withEmptyDatabase_shouldReturnZero(self):
        component_under_test = db.Database('test_database')

        assert component_under_test.anzahl_stechzeiten() == 0

    def test_anzahlStechzeiten(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_stechzeit(date.today(), time('0:0'), time('1:23'), 'Datev')

        assert component_under_test.anzahl_stechzeiten() == 1



class soll_zeit(unittest.TestCase):

    def test_edit(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_soll_zeit(datum('1/2/2003'), datum('4/5/2006'), laenge('1:23'), 'DATEV')

        component_under_test.edit_sollzeit(0, datum('7/8/2009'), datum('10/11/2012'), laenge('4:56'), 'DATEV')

        assert component_under_test.soll_zeiten.Startdatum[0] == datum('7/8/2009')
        assert component_under_test.soll_zeiten.Endedatum[0] == datum('10/11/2012')
        assert component_under_test.soll_zeiten.Dauer[0] == laenge('4:56')

    def test_add(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_soll_zeit(datum('7/8/2009'), datum('10/11/2012'), laenge('4:56'), 'DATEV')

        assert component_under_test.soll_zeiten.Startdatum[0] == datum('7/8/2009')
        assert component_under_test.soll_zeiten.Endedatum[0] == datum('10/11/2012')
        assert component_under_test.soll_zeiten.Dauer[0] == laenge('4:56')

    def test_getSollzeitenList_withEmptyDB_shouldReturnEmptyList(self):
        component_under_test = db.Database('test_database')
        assert component_under_test.get_sollzeiten_liste() == []

    def test_getSollzeitenList_withOneElementInDB_shouldReturnListWithElement(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_soll_zeit(datum('7/8/2009'), datum('10/11/2012'), laenge('4:56'), 'DATEV')

        assert len(component_under_test.get_sollzeiten_liste()) == 1
        assert component_under_test.get_sollzeiten_liste()[0]['index'] == 0
        assert component_under_test.get_sollzeiten_liste()[0]['Startdatum'] == datum('7/8/2009')
        assert component_under_test.get_sollzeiten_liste()[0]['Endedatum'] == datum('10/11/2012')
        assert component_under_test.get_sollzeiten_liste()[0]['Dauer'] == laenge('4:56')
        assert component_under_test.get_sollzeiten_liste()[0]['Arbeitgeber'] == 'DATEV'



class sonder_zeiten_test(unittest.TestCase):
    def  test_add_sonder_zeiten(self):
        component_under_test = Database('test_database')


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


class sonder_zeiten(unittest.TestCase):
    def test_add(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_sonder_zeit(datum('01/01/2017'), time('10:00'), 'test', 'test')

        assert len(component_under_test.sonder_zeiten) == 1

    def test_get_soll_ist_ueberischt_withSonderzeit_und_stechzeit_shouldReturnCummulatedResult(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_stechzeit(date.today(), time('0:0'), time('1:23'), 'Datev')
        component_under_test.add_sonder_zeit(date.today(), time('4:00'), 'urlaub', 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(date.today().year)
        print(result[date.today().isocalendar()[1]])
        assert len(result.keys()) == 1
        assert result.keys() == set([date.today().isocalendar()[1]])
        assert result[date.today().isocalendar()[1]] == (timedelta(hours=5, minutes=23), _zero())

class refresh(unittest.TestCase):
    def teste_refresh_with_empty_database(self):
        component_under_test = db.Database('test_database')
        component_under_test.refresh()

    def teste_refresh_shouldAddEinzelbuchungenVonDauerauftrag(self):
        component_under_test = db.Database('test_database')
        component_under_test.dauerauftraege.add(datum('10/01/2010'), datum('11/03/2010'), '', '', 'monatlich', 20)
        component_under_test.refresh()

        assert len(component_under_test.einzelbuchungen.content) == 3
        assert component_under_test.einzelbuchungen.get_jahreseinnahmen(2010) == 60

if __name__ == '__main__':
    unittest.main()
