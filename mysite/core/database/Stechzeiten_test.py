'''
Created on 11.08.2017

@author: sebastian
'''
from datetime import date, timedelta
import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../../')

from core.DatabaseModule import Database
from core.database.Stechzeiten import Stechzeiten
from viewcore.converter import laenge, datum, time


_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../../')

def _zero():
    return timedelta(minutes=0)

class stechzeiten(unittest.TestCase):

    def teste_add(self):
        component_under_test = Stechzeiten()

        component_under_test.add(date.today(), time('0:0'), time('1:23'), 'Datev')

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Datum[0] == date.today()
        assert component_under_test.content.Einstechen[0] == time('0:0')
        assert component_under_test.content.Ausstechen[0] == time('1:23')
        assert component_under_test.content.Arbeitgeber[0] == 'Datev'

    def teste_stechzeitenVorhanden_withNoExistingStechzeit_shouldReturnFalse(self):
        component_under_test = Database('test_database')
        assert not component_under_test.stechzeiten_vorhanden()

    def teste_stechzeitenVorhanden_withOneExisitingStechzeit_shouldReturnTrue(self):
        component_under_test = Database('test_database')
        component_under_test.stechzeiten.add(date.today(), time('2:3'), time('6:32'), 'BlaBla')

        assert component_under_test.stechzeiten_vorhanden()



    def teste_edit(self):
        component_under_test = Stechzeiten()
        component_under_test.add(date.today(), time('2:3'), time('6:32'), 'BlaBla')

        component_under_test.edit(0, date.today(), time('0:0'), time('1:23'), 'Datev')


        assert len(component_under_test.content) == 1
        assert component_under_test.content.Datum[0] == date.today()
        assert component_under_test.content.Einstechen[0] == time('0:0')
        assert component_under_test.content.Ausstechen[0] == time('1:23')
        assert component_under_test.content.Arbeitgeber[0] == 'Datev'


    def test_withOnlyOneStechzeit_shouldReturnWeekOfTodayWithTimdelta(self):
        component_under_test = Database('test_database')
        component_under_test.stechzeiten.add(date.today(), time('0:0'), time('1:23'), 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        assert len(result.keys()) == 1
        assert result.keys() == set([date.today().isocalendar()[1]])
        assert result[date.today().isocalendar()[1]] == (timedelta(hours=1, minutes=23), _zero())

    def test_withTwoStechzeitInSameWeek_shouldReturnCummulatedResult(self):
        component_under_test = Database('test_database')
        component_under_test.stechzeiten.add(date.today(), time('0:0'), time('1:23'), 'Datev')
        component_under_test.stechzeiten.add(date.today(), time('0:0'), time('1:23'), 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        assert len(result.keys()) == 1
        assert result.keys() == set([date.today().isocalendar()[1]])
        assert result[date.today().isocalendar()[1]] == (timedelta(hours=2, minutes=46), _zero())

    def test_withTwoStechzeitInDifferendWeeks_shouldReturnTwoResults(self):
        component_under_test = Database('test_database')
        component_under_test.stechzeiten.add(date.today(), time('0:0'), time('1:23'), 'Datev')
        component_under_test.stechzeiten.add(date.today() - timedelta(days=7), time('0:0'), time('1:23'), 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        assert len(result.keys()) == 2
        assert result.keys() == set([date.today().isocalendar()[1], date.today().isocalendar()[1] - 1])
        assert result[date.today().isocalendar()[1]] == (timedelta(hours=1, minutes=23), _zero())
        assert result[date.today().isocalendar()[1] - 1] == (timedelta(hours=1, minutes=23), _zero())

    def test_sollzeitOfFirtstWeekday_shouldReturnWeekOfTodayWithSollzeit(self):
        component_under_test = Database('test_database')

        component_under_test.sollzeiten.add(datum('29/05/2017'), datum('29/05/2017'), time('1:02'), 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(datum('29/05/2017').year)

        assert datum('29/05/2017').isocalendar()[1] in result
        assert result[datum('29/05/2017').isocalendar()[1]] == (_zero(), timedelta(hours=1, minutes=2))

    def test_sollzeitOfLastWeekday_shouldReturnWeekOfTodayWithSollzeit(self):
        component_under_test = Database('test_database')

        component_under_test.sollzeiten.add(datum('02/06/2017'), datum('02/06/2017'), time('1:02'), 'Datev')
        result = component_under_test.get_soll_ist_uebersicht(datum('02/06/2017').year)

        assert datum('02/06/2017').isocalendar()[1] in result
        assert result[datum('02/06/2017').isocalendar()[1]] == (_zero(), timedelta(hours=1, minutes=2))

    def test_withTwoSollzeiten_shouldReturnCummulatedResults(self):
        component_under_test = Database('test_database')

        component_under_test.sollzeiten.add(datum('16/5/2017'), datum('16/5/2017'), time('1:02'), 'Datev')
        component_under_test.sollzeiten.add(datum('15/5/2017'), datum('15/5/2017'), time('0:30'), 'Datev')

        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        print(result)
        assert datum('16/5/2017').isocalendar()[1] in result.keys()
        assert result[datum('16/5/2017').isocalendar()[1]] == (_zero(), timedelta(hours=1, minutes=32))

    def test_withTwosollzeiten_add_SameDate_shouldReturnCummulatedResults(self):
        component_under_test = Database('test_database')

        component_under_test.sollzeiten.add(datum('01/06/2017'), datum('01/06/2017'), time('1:02'), 'Datev')
        component_under_test.sollzeiten.add(datum('01/06/2017'), datum('01/06/2017'), time('0:30'), 'Datev')

        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        assert datum('01/06/2017').isocalendar()[1] in result
        assert result[datum('01/06/2017').isocalendar()[1]] == (_zero(), timedelta(hours=1, minutes=32))

    def test_withWochenSollzeit_shouldIgnoreWochenende(self):
        component_under_test = Database('test_database')

        component_under_test.sollzeiten.add(datum('15/5/2017'), datum('21/5/2017'), time('1:02'), 'Datev')

        result = component_under_test.get_soll_ist_uebersicht(date.today().year)

        assert datum('15/5/2017').isocalendar()[1] in result.keys()
        assert result[datum('15/5/2017').isocalendar()[1]] == (_zero(), timedelta(hours=5, minutes=10))


    def test_anzahlStechzeiten_withEmptyDatabase_shouldReturnZero(self):
        component_under_test = Database('test_database')

        assert component_under_test.anzahl_stechzeiten() == 0

    def test_anzahlStechzeiten(self):
        component_under_test = Database('test_database')
        component_under_test.stechzeiten.add(date.today(), time('0:0'), time('1:23'), 'Datev')

        assert component_under_test.anzahl_stechzeiten() == 1



