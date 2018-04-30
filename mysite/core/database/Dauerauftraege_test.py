'''
Created on 11.08.2017

@author: sebastian
'''
from datetime import date
import os
import sys
import unittest

import core.DatabaseModule as db
from core.database.Dauerauftraege import Dauerauftraege
from core.database.Einzelbuchungen import Einzelbuchungen
from viewcore.converter import datum

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../../')


class DauerauftraegeTest(unittest.TestCase):

    def test_add_shouldTaint(self):
        component_under_test = Dauerauftraege()
        assert component_under_test.taint_number() == 0
        component_under_test.add(
            datum('1.1.2010'),
            date.today(),
            'some kategorie',
            'some name',
            'some rhythmus',
            1.23)
        assert component_under_test.taint_number() == 1

    def test_edit_shouldTaint(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(
            datum('1.1.2010'),
            date.today(),
            'some kategorie',
            'some name',
            'some rhythmus',
            1.23)
        component_under_test.de_taint()
        assert component_under_test.taint_number() == 0
        component_under_test.edit(
            0,
            datum('2.1.2010'),
            datum('3.1.2010'),
            'some other kategorie',
            'some other name',
            'some other rhythmus',
            2.34)
        assert component_under_test.taint_number() == 1

    def test_delete_shouldTaint(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(
            datum('1.1.2010'),
            date.today(),
            'some kategorie',
            'some name',
            'some rhythmus',
            1.23)
        component_under_test.de_taint()
        assert component_under_test.taint_number() == 0
        component_under_test.delete(0)
        assert component_under_test.taint_number() == 1

    def test_get(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(
            datum('1.1.2010'),
            date.today(),
            'some kategorie',
            'some name',
            'some rhythmus',
            1.23)

        result = component_under_test.get(0)

        assert len(component_under_test.content) == 1
        assert result['Startdatum'] == datum('1.1.2010')
        assert result['Endedatum'] == date.today()
        assert result['Name'] == 'some name'
        assert result['Kategorie'] == 'some kategorie'
        assert result['Rhythmus'] == 'some rhythmus'
        assert result['Wert'] == 1.23

    def test_add(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(
            datum('1.1.2010'),
            date.today(),
            'some kategorie',
            'some name',
            'some rhythmus',
            1.23)

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Startdatum[0] == datum('1.1.2010')
        assert component_under_test.content.Endedatum[0] == date.today()
        assert component_under_test.content.Name[0] == 'some name'
        assert component_under_test.content.Kategorie[0] == 'some kategorie'
        assert component_under_test.content.Rhythmus[0] == 'some rhythmus'
        assert component_under_test.content.Wert[0] == 1.23

    def test_aendere_beiLeererDatenbank(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(
            datum('1.1.2010'),
            date.today(),
            'some kategorie',
            'some name',
            'some rhythmus',
            1.23)
        component_under_test.edit(
            0,
            datum('2.1.2010'),
            datum('3.1.2010'),
            'some other kategorie',
            'some other name',
            'some other rhythmus',
            2.34)

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Startdatum[0] == datum('2.1.2010')
        assert component_under_test.content.Endedatum[0] == datum('3.1.2010')
        assert component_under_test.content.Name[0] == 'some other name'
        assert component_under_test.content.Kategorie[0] == 'some other kategorie'
        assert component_under_test.content.Rhythmus[0] == 'some other rhythmus'
        assert component_under_test.content.Wert[0] == 2.34

    def test_aendere_beiVollerDatenbank(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(
            datum('1.1.2010'),
            date.today(),
            '1some kategorie',
            '1some name',
            '1some rhythmus',
            1.23)
        component_under_test.add(
            datum('1.1.2010'),
            date.today(),
            '2some kategorie',
            '2some name',
            '2some rhythmus',
            1.23)
        component_under_test.add(
            datum('1.1.2010'),
            date.today(),
            '3some kategorie',
            '3some name',
            '3some rhythmus',
            1.23)

        component_under_test.edit(
            1,
            datum('2.1.2010'),
            datum('3.1.2010'),
            'some other kategorie',
            'some other name',
            'some other rhythmus',
            2.34)

        assert len(component_under_test.content) == 3
        assert component_under_test.content.Startdatum[1] == datum('2.1.2010')
        assert component_under_test.content.Endedatum[1] == datum('3.1.2010')
        assert component_under_test.content.Name[1] == 'some other name'
        assert component_under_test.content.Kategorie[1] == 'some other kategorie'
        assert component_under_test.content.Rhythmus[1] == 'some other rhythmus'
        assert component_under_test.content.Wert[1] == 2.34

    def test_get_aktuelle_withActualDauerauftrag_shouldReturnDauerauftrag(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(datum('01.01.2012'), datum('01.01.2100'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.aktuelle()

        assert len(result) == 1
        assert result[0]['Startdatum'] == datum('01.01.2012')
        assert result[0]['Endedatum'] == datum('01.01.2100')
        assert result[0]['Kategorie'] == 'some kategorie'
        assert result[0]['Name'] == 'some name'
        assert result[0]['Rhythmus'] == 'some rhythmus'
        assert result[0]['Wert'] == 1

    def test_get_aktuelle_withPastDauerauftrag_shouldReturnEmptyList(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(datum('01.01.2012'), datum('01.01.2012'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.aktuelle()

        assert result == []

    def test_get_aktuelle_withFutureDauerauftrag_shouldReturnEmptyList(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(datum('01.01.2100'), datum('01.01.2100'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.aktuelle()

        assert result == []

    def test_get_past_withPastDauerauftrag_shouldReturnDauerauftrag(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(datum('01.01.2012'), datum('01.01.2012'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.past()

        assert len(result) == 1
        assert result[0]['Startdatum'] == datum('01.01.2012')
        assert result[0]['Endedatum'] == datum('01.01.2012')
        assert result[0]['Kategorie'] == 'some kategorie'
        assert result[0]['Name'] == 'some name'
        assert result[0]['Rhythmus'] == 'some rhythmus'
        assert result[0]['Wert'] == 1

    def test_get_past_withActualDauerauftrag_shouldReturnEmptyList(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(datum('01.01.2012'), datum('01.01.2100'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.past()

        assert result == []

    def test_get_future_withActualDauerauftrag_shouldReturnEmptyList(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(datum('01.01.2012'), datum('01.01.2100'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.future()

        assert result == []

    def test_get_future_withFutureDauerauftrag_shouldReturnDauerauftrag(self):
        component_under_test = Dauerauftraege()
        component_under_test.add(datum('01.01.2100'), datum('01.01.2100'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.future()

        assert len(result) == 1
        assert result[0]['Startdatum'] == datum('01.01.2100')
        assert result[0]['Endedatum'] == datum('01.01.2100')
        assert result[0]['Kategorie'] == 'some kategorie'
        assert result[0]['Name'] == 'some name'
        assert result[0]['Rhythmus'] == 'some rhythmus'
        assert result[0]['Wert'] == 1
