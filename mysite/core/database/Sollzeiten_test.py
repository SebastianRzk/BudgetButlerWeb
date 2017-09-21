'''
Created on 11.08.2017

@author: sebastian
'''
from datetime import date
import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../../')

from core.DatabaseModule import Database
from core.database.Sollzeiten import Sollzeiten
from viewcore.converter import laenge, datum





class soll_zeit(unittest.TestCase):

    def test_edit(self):
        component_under_test = Sollzeiten()
        component_under_test.add(datum('1/2/2003'), datum('4/5/2006'), laenge('1:23'), 'DATEV')

        component_under_test.edit(0, datum('7/8/2009'), datum('10/11/2012'), laenge('4:56'), 'DATEV')

        assert component_under_test.content.Startdatum[0] == datum('7/8/2009')
        assert component_under_test.content.Endedatum[0] == datum('10/11/2012')
        assert component_under_test.content.Dauer[0] == laenge('4:56')

    def test_add(self):
        component_under_test = Sollzeiten()
        component_under_test.add(datum('7/8/2009'), datum('10/11/2012'), laenge('4:56'), 'DATEV')

        assert component_under_test.content.Startdatum[0] == datum('7/8/2009')
        assert component_under_test.content.Endedatum[0] == datum('10/11/2012')
        assert component_under_test.content.Dauer[0] == laenge('4:56')

    def test_getSollzeitenList_withEmptyDB_shouldReturnEmptyList(self):
        component_under_test = Sollzeiten()
        assert component_under_test.get_sollzeiten_liste() == []

    def test_getSollzeitenList_withOneElementInDB_shouldReturnListWithElement(self):
        component_under_test = Sollzeiten()
        component_under_test.add(datum('7/8/2009'), datum('10/11/2012'), laenge('4:56'), 'DATEV')

        assert len(component_under_test.get_sollzeiten_liste()) == 1
        assert component_under_test.get_sollzeiten_liste()[0]['index'] == 0
        assert component_under_test.get_sollzeiten_liste()[0]['Startdatum'] == datum('7/8/2009')
        assert component_under_test.get_sollzeiten_liste()[0]['Endedatum'] == datum('10/11/2012')
        assert component_under_test.get_sollzeiten_liste()[0]['Dauer'] == laenge('4:56')
        assert component_under_test.get_sollzeiten_liste()[0]['Arbeitgeber'] == 'DATEV'

