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
        component_under_test.sonderzeiten.add(datum('01/01/2017'), time('10:00'), 'test', 'test')

        assert len(component_under_test.sonderzeiten.content) == 1

    def test_get_soll_ist_ueberischt_withSonderzeit_und_stechzeit_shouldReturnCummulatedResult(self):
        component_under_test = db.Database('test_database')
        component_under_test.stechzeiten.add(date.today(), time('0:0'), time('1:23'), 'Datev')
        component_under_test.sonderzeiten.add(date.today(), time('4:00'), 'urlaub', 'Datev')
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

if __name__ == '__main__':
    unittest.main()
