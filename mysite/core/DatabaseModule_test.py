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

class einzelbuchungen(unittest.TestCase):

    def test_getJahresausgaben_withEmptyDatabase_shouldReturnZero(self):
        component_under_test = db.Database('test_database')
        assert component_under_test.get_jahresausgaben(2016) == 0

    def test_getJahresausgaben_withNonMatchingDate_shouldReturnZero(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/1990'), 'some kategorie', 'some name', -1.54)
        assert component_under_test.get_jahresausgaben(2016) == 0

    def test_getJahresausgaben_withNonMatchingValue_shouldReturnZero(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2016'), 'some kategorie', 'some name', 1.54)
        assert component_under_test.get_jahresausgaben(2016) == 0

    def test_getJahreseinnahmen_withEmptyDatabase_shouldReturnZero(self):
        component_under_test = db.Database('test_database')
        assert component_under_test.get_jahreseinnahmen(2016) == 0

    def test_getJahreseinnahmen_withNonMatchingDate_shouldReturnZero(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/1990'), 'some kategorie', 'some name', -1.54)
        assert component_under_test.get_jahreseinnahmen(2016) == 0

    def test_getJahreseinnahmen_withNonMatchingValue_shouldReturnZero(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2016'), 'some kategorie', 'some name', -1.54)
        assert component_under_test.get_jahreseinnahmen(2016) == 0



    def test_add(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(date.today(), 'some kategorie', 'some name', 1.54)

        assert len(component_under_test.einzelbuchungen) == 1
        assert component_under_test.einzelbuchungen.Datum[0] == date.today()
        assert component_under_test.einzelbuchungen.Name[0] == 'some name'
        assert component_under_test.einzelbuchungen.Kategorie[0] == 'some kategorie'
        assert component_under_test.einzelbuchungen.Wert[0] == 1.54
        assert component_under_test.einzelbuchungen.Tags[0] == []

    def test_aendere_beiEinzigerEinzelbuchung(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(date.today(), 'some kategorie', 'some name', 1.54)
        component_under_test.edit_einzelbuchung(0, date.today(), 'some other kategorie', 'some other name', 2.65)

        assert len(component_under_test.einzelbuchungen) == 1
        assert component_under_test.einzelbuchungen.Datum[0] == date.today()
        assert component_under_test.einzelbuchungen.Name[0] == 'some other name'
        assert component_under_test.einzelbuchungen.Kategorie[0] == 'some other kategorie'
        assert component_under_test.einzelbuchungen.Wert[0] == 2.65


    def test_aendere_beiVollerDatenbank(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2017'), '3kategorie', '3name', 1.54)
        component_under_test.add_einzelbuchung(datum('02/01/2017'), '2kategorie', '2name', 1.54)
        component_under_test.add_einzelbuchung(datum('03/01/2017'), '1kategorie', '1name', 1.54)

        assert component_under_test.einzelbuchungen.Datum[0] == datum('01/01/2017')

        component_under_test.edit_einzelbuchung(0, datum('15/01/2017'), 'some other kategorie', 'some other name', 2.65)

        assert len(component_under_test.einzelbuchungen) == 3
        assert set(component_under_test.einzelbuchungen.Name) == set(['1name', '2name', 'some other name'])
        assert set(component_under_test.einzelbuchungen.Datum) == set([datum('02/01/2017'), datum('03/01/2017'), datum('15/01/2017')])

        changed_row = component_under_test.einzelbuchungen[component_under_test.einzelbuchungen.Datum == datum('15/01/2017')]
        changed_row.reset_index(drop=True, inplace=True)
        assert changed_row.Name[0] == 'some other name'
        assert changed_row.Kategorie[0] == 'some other kategorie'
        assert changed_row.Wert[0] == 2.65

    def test_get_single_einzelbuchung(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(date.today(), '1kategorie', '1name', 1.54)

        result = component_under_test.get_single_einzelbuchung(0)

        assert result['index'] == 0
        assert result['Datum'] == date.today()
        assert result['Name'] == '1name'
        assert result['Kategorie'] == '1kategorie'
        assert result['Wert'] == 1.54

    def test_get_gesamtausgaben_nach_kategorie_withEmptyDatabase_shouldReturnEmptyDict(self):
        component_under_test = db.Database('test_database')

        assert component_under_test.get_gesamtausgaben_nach_kategorie() == {}

    def test_get_gesamtausgaben_nach_kategorie_shouldReturnResult(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(date.today(), '1kategorie', '1name', -1)
        component_under_test.add_einzelbuchung(date.today(), '1kategorie', '1name', -4)
        component_under_test.add_einzelbuchung(date.today(), '2kategorie', '1name', -3)

        result = component_under_test.get_gesamtausgaben_nach_kategorie()
        assert result.keys() == set(['1kategorie', '2kategorie'])
        assert result['1kategorie'] == -5
        assert result['2kategorie'] == -3

    def test_get_gesamtausgaben_nach_kategorie_withEinnahmen_shouldFilterEinnahmen(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(date.today(), '1kategorie', '1name', 1)

        assert component_under_test.get_gesamtausgaben_nach_kategorie() == {}

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2012'), '1kategorie', '1name', 1)
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '1kategorie', '1name', 1)
        component_under_test.add_einzelbuchung(datum('01/01/2013'), '1kategorie', '1name', 1)

        assert component_under_test.get_sortierte_einzelbuchungen().Datum[0].year == 2011
        assert component_under_test.get_sortierte_einzelbuchungen().Datum[1].year == 2012
        assert component_under_test.get_sortierte_einzelbuchungen().Datum[2].year == 2013

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum_Kategorie(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '1kategorie', '1name', 1)
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '3kategorie', '1name', 1)
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '2kategorie', '1name', 1)

        assert component_under_test.get_sortierte_einzelbuchungen().Kategorie[0] == '1kategorie'
        assert component_under_test.get_sortierte_einzelbuchungen().Kategorie[1] == '2kategorie'
        assert component_under_test.get_sortierte_einzelbuchungen().Kategorie[2] == '3kategorie'

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum_Kategorie_Name(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '1kategorie', '1name', 1)
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '1kategorie', '3name', 1)
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '1kategorie', '2name', 1)

        assert component_under_test.get_sortierte_einzelbuchungen().Name[0] == '1name'
        assert component_under_test.get_sortierte_einzelbuchungen().Name[1] == '2name'
        assert component_under_test.get_sortierte_einzelbuchungen().Name[2] == '3name'

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum_Kategorie_Name_Wert(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '1kategorie', '1name', 1)
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '1kategorie', '1name', 10)
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '1kategorie', '1name', 5)

        assert component_under_test.get_sortierte_einzelbuchungen().Wert[0] == 1
        assert component_under_test.get_sortierte_einzelbuchungen().Wert[1] == 5
        assert component_under_test.get_sortierte_einzelbuchungen().Wert[2] == 10



    def test_edit_einzelbuchung_shouldRefreshSortingOfEinzelbuchungen(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2012'), '1kategorie', '1name', 1)
        component_under_test.add_einzelbuchung(datum('01/01/2011'), '1kategorie', '1name', 1)
        component_under_test.add_einzelbuchung(datum('01/01/2013'), '1kategorie', '1name', 1)

        component_under_test.edit_einzelbuchung(0, datum('01/01/2020'), '1kategorie', '1name', 1)

        assert component_under_test.get_sortierte_einzelbuchungen().Datum[0].year == 2012
        assert component_under_test.get_sortierte_einzelbuchungen().Datum[1].year == 2013
        assert component_under_test.get_sortierte_einzelbuchungen().Datum[2].year == 2020


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


class dauerauftraege(unittest.TestCase):

    def test_get_single(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(
            datum('1/1/2010'),
            date.today(),
            'some kategorie',
            'some name',
            'some rhythmus',
            1.23)

        result = component_under_test.get_single_dauerauftrag(0)

        assert len(component_under_test.dauerauftraege) == 1
        assert result['Startdatum'] == datum('1/1/2010')
        assert result['Endedatum'] == date.today()
        assert result['Name'] == 'some name'
        assert result['Kategorie'] == 'some kategorie'
        assert result['Rhythmus'] == 'some rhythmus'
        assert result['Wert'] == 1.23


    def test_add(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(
            datum('1/1/2010'),
            date.today(),
            'some kategorie',
            'some name',
            'some rhythmus',
            1.23)

        assert len(component_under_test.dauerauftraege) == 1
        assert component_under_test.dauerauftraege.Startdatum[0] == datum('1/1/2010')
        assert component_under_test.dauerauftraege.Endedatum[0] == date.today()
        assert component_under_test.dauerauftraege.Name[0] == 'some name'
        assert component_under_test.dauerauftraege.Kategorie[0] == 'some kategorie'
        assert component_under_test.dauerauftraege.Rhythmus[0] == 'some rhythmus'
        assert component_under_test.dauerauftraege.Wert[0] == 1.23


    def test_aendere_beiLeererDatenbank(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(
            datum('1/1/2010'),
            date.today(),
            'some kategorie',
            'some name',
            'some rhythmus',
            1.23)
        component_under_test.edit_dauerauftrag(
            0,
            datum('2/1/2010'),
            datum('3/1/2010'),
            'some other kategorie',
            'some other name',
            'some other rhythmus',
            2.34)

        assert len(component_under_test.dauerauftraege) == 1
        assert component_under_test.dauerauftraege.Startdatum[0] == datum('2/1/2010')
        assert component_under_test.dauerauftraege.Endedatum[0] == datum('3/1/2010')
        assert component_under_test.dauerauftraege.Name[0] == 'some other name'
        assert component_under_test.dauerauftraege.Kategorie[0] == 'some other kategorie'
        assert component_under_test.dauerauftraege.Rhythmus[0] == 'some other rhythmus'
        assert component_under_test.dauerauftraege.Wert[0] == 2.34


    def test_aendere_beiVollerDatenbank(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(
            datum('1/1/2010'),
            date.today(),
            '1some kategorie',
            '1some name',
            '1some rhythmus',
            1.23)
        component_under_test.add_dauerauftrag(
            datum('1/1/2010'),
            date.today(),
            '2some kategorie',
            '2some name',
            '2some rhythmus',
            1.23)
        component_under_test.add_dauerauftrag(
            datum('1/1/2010'),
            date.today(),
            '3some kategorie',
            '3some name',
            '3some rhythmus',
            1.23)

        component_under_test.edit_dauerauftrag(
            1,
            datum('2/1/2010'),
            datum('3/1/2010'),
            'some other kategorie',
            'some other name',
            'some other rhythmus',
            2.34)

        assert len(component_under_test.dauerauftraege) == 3
        assert component_under_test.dauerauftraege.Startdatum[1] == datum('2/1/2010')
        assert component_under_test.dauerauftraege.Endedatum[1] == datum('3/1/2010')
        assert component_under_test.dauerauftraege.Name[1] == 'some other name'
        assert component_under_test.dauerauftraege.Kategorie[1] == 'some other kategorie'
        assert component_under_test.dauerauftraege.Rhythmus[1] == 'some other rhythmus'
        assert component_under_test.dauerauftraege.Wert[1] == 2.34


    def test_get_aktuelle_withActualDauerauftrag_shouldReturnDauerauftrag(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(datum('01/01/2012'), datum('01/01/2100'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.aktuelle_dauerauftraege()

        assert len(result) == 1
        assert result[0]['Startdatum'] == datum('01/01/2012')
        assert result[0]['Endedatum'] == datum('01/01/2100')
        assert result[0]['Kategorie'] == 'some kategorie'
        assert result[0]['Name'] == 'some name'
        assert result[0]['Rhythmus'] == 'some rhythmus'
        assert result[0]['Wert'] == 1

    def test_get_aktuelle_withPastDauerauftrag_shouldReturnEmptyList(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(datum('01/01/2012'), datum('01/01/2012'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.aktuelle_dauerauftraege()

        assert result == []

    def test_get_aktuelle_withFutureDauerauftrag_shouldReturnEmptyList(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(datum('01/01/2100'), datum('01/01/2100'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.aktuelle_dauerauftraege()

        assert result == []

    def test_get_past_withPastDauerauftrag_shouldReturnDauerauftrag(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(datum('01/01/2012'), datum('01/01/2012'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.past_dauerauftraege()

        assert len(result) == 1
        assert result[0]['Startdatum'] == datum('01/01/2012')
        assert result[0]['Endedatum'] == datum('01/01/2012')
        assert result[0]['Kategorie'] == 'some kategorie'
        assert result[0]['Name'] == 'some name'
        assert result[0]['Rhythmus'] == 'some rhythmus'
        assert result[0]['Wert'] == 1


    def test_get_past_withActualDauerauftrag_shouldReturnEmptyList(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(datum('01/01/2012'), datum('01/01/2100'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.past_dauerauftraege()

        assert result == []

    def test_get_future_withActualDauerauftrag_shouldReturnEmptyList(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(datum('01/01/2012'), datum('01/01/2100'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.future_dauerauftraege()

        assert result == []

    def test_get_future_withFutureDauerauftrag_shouldReturnDauerauftrag(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_dauerauftrag(datum('01/01/2100'), datum('01/01/2100'), 'some kategorie', 'some name', 'some rhythmus', 1)

        result = component_under_test.future_dauerauftraege()

        assert len(result) == 1
        assert result[0]['Startdatum'] == datum('01/01/2100')
        assert result[0]['Endedatum'] == datum('01/01/2100')
        assert result[0]['Kategorie'] == 'some kategorie'
        assert result[0]['Name'] == 'some name'
        assert result[0]['Rhythmus'] == 'some rhythmus'
        assert result[0]['Wert'] == 1


class gesamtausgaben_jahr(unittest.TestCase):

    def test_get_gesamtausgaben_jahr_withOneAusgabe_shouldReturnAusgabe(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(date.today(), 'Some Kategorie', 'bla', -1)

        result = component_under_test.get_gesamtausgaben_jahr(date.today().year)

        assert result.index == ['Some Kategorie']
        assert result.Wert[0] == -1

    def test_get_gesamtausgaben_jahr_withOneAusgabeAndOneEinnahme_shouldReturnOnlyAusgabe(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(date.today(), 'Some Kategorie', 'bla', -1)
        component_under_test.add_einzelbuchung(date.today(), 'Some Kategorie', 'bla', 11)

        result = component_under_test.get_gesamtausgaben_jahr(date.today().year)

        assert result.index == ['Some Kategorie']
        assert result.Wert[0] == -1

    def test_get_gesamtausgaben_jahr_withOneAusgabeAndOneAusgabeWithWrongYear_shouldReturnOnlyAusgabeOfMatchingYear(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2017'), 'Some Kategorie', 'bla', -1)
        component_under_test.add_einzelbuchung(datum('01/01/2014'), 'Some Kategorie', 'bla', -1)

        result = component_under_test.get_gesamtausgaben_jahr(2017)

        assert result.index == ['Some Kategorie']
        print(result)
        assert result.Wert[0] == -1

    def test_get_gesamtausgaben_jahr_withTwoDifferentCategories_shouldReturnBothCategories(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2017'), 'Some Kategorie', 'bla', -1)
        component_under_test.add_einzelbuchung(datum('01/01/2017'), 'Some other Kategorie', 'bla', -1)

        result = component_under_test.get_gesamtausgaben_jahr(2017)

        assert set(result.index) == set(['Some Kategorie', 'Some other Kategorie'])

    def test_get_gesamtausgaben_jahr_withTwoDifferentDates_shouldReturnCummulatedResult(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2017'), 'Some Kategorie', 'bla', -1)
        component_under_test.add_einzelbuchung(datum('01/01/2017'), 'Some Kategorie', 'bla', -3)

        result = component_under_test.get_gesamtausgaben_jahr(2017)

        assert result.index == ['Some Kategorie']
        assert result.Wert[0] == -4

    def test_get_gesamtausgaben_jahr_withEmptyDB_shouldReturnEmptyDataframe(self):
        component_under_test = db.Database('test_database')

        result = component_under_test.get_gesamtausgaben_jahr(2017)

        assert set(result.index) == set()

    def test_get_jahresausgaben_nach_monat_withEmptyDB_shouldReturnEmptyDataframe(self):
        component_under_test = db.Database('test_database')

        result = component_under_test.get_jahresausgaben_nach_monat(2017)

        assert set(result.index) == set()

    def test_getGesamtausgabenNachKategorieProzentual_withEmptyDB_shouldReturnEmptyDict(self):
        component_under_test = db.Database('test_database')

        result = component_under_test.get_gesamtausgaben_nach_kategorie_prozentual()

        assert result == {}

    def test_getGesamtausgabenNachKategorieProzentual_withEinnahme_shouldReturnEmptyDict(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2015'), 'kategorie 1', 'some name', 10)

        result = component_under_test.get_gesamtausgaben_nach_kategorie_prozentual()

        assert result == {}

    def test_getGesamtausgabenNachKategorieProzentual_withOneEntry_shouldReturnKategorieWith100Percent(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2015'), 'kategorie 1', 'some name', -10)

        result = component_under_test.get_gesamtausgaben_nach_kategorie_prozentual()

        assert set(result.keys()) == set(['kategorie 1'])
        assert  result['kategorie 1'] == 100.00

    def test_getGesamtausgabenNachKategorieProzentual_withTwoEntrys_shouldReturnResult(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2015'), 'kategorie 1', 'some name', -7.5)
        component_under_test.add_einzelbuchung(datum('01/01/2015'), 'kategorie 2', 'some name', -2.5)

        result = component_under_test.get_gesamtausgaben_nach_kategorie_prozentual()

        assert set(result.keys()) == set(['kategorie 1', 'kategorie 2'])
        assert  result['kategorie 1'] == 75.00
        assert  result['kategorie 2'] == 25.00

    def test_getJahresausgabenNachKategorieProzentual_withEmptyDB_shouldReturnEmptyDict(self):
        component_under_test = db.Database('test_database')

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert result == {}

    def test_getJahresausgabenNachKategorieProzentual_withEinnahme_shouldReturnEmptyDict(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2015'), 'kategorie 1', 'some name', 10)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert result == {}


    def test_getJahresausgabenNachKategorieProzentual_withAusgabeAußerhalbDesJahres_shouldReturnEmptyDict(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2014'), 'kategorie 1', 'some name', -10)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert result == {}

    def test_getJahresausgabenNachKategorieProzentual_withOneEntry_shouldReturnKategorieWith100Percent(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2015'), 'kategorie 1', 'some name', -10)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert set(result.keys()) == set(['kategorie 1'])
        assert  result['kategorie 1'] == 100.00

    def test_getJahresausgabenNachKategorieProzentual_withTwoEntrys_shouldReturnResult(self):
        component_under_test = db.Database('test_database')
        component_under_test.add_einzelbuchung(datum('01/01/2015'), 'kategorie 1', 'some name', -7.5)
        component_under_test.add_einzelbuchung(datum('01/01/2015'), 'kategorie 2', 'some name', -2.5)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert set(result.keys()) == set(['kategorie 1', 'kategorie 2'])
        assert  result['kategorie 1'] == 75.00
        assert  result['kategorie 2'] == 25.00

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

if __name__ == '__main__':
    unittest.main()
