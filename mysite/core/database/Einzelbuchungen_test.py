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

import core.DatabaseModule as db
from core.database.Einzelbuchungen import Einzelbuchungen
from viewcore.converter import datum


class einzelbuchungen(unittest.TestCase):

    def test_add(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), 'some kategorie', 'some name', 1.54)

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Datum[0] == date.today()
        assert component_under_test.content.Name[0] == 'some name'
        assert component_under_test.content.Kategorie[0] == 'some kategorie'
        assert component_under_test.content.Wert[0] == 1.54
        assert component_under_test.content.Tags[0] == []

    def test_aendere_beiEinzigerEinzelbuchung(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), 'some kategorie', 'some name', 1.54)
        component_under_test.edit(0, date.today(), 'some other kategorie', 'some other name', 2.65)

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Datum[0] == date.today()
        assert component_under_test.content.Name[0] == 'some other name'
        assert component_under_test.content.Kategorie[0] == 'some other kategorie'
        assert component_under_test.content.Wert[0] == 2.65


    def test_aendere_beiVollerDatenbank(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2017'), '3kategorie', '3name', 1.54)
        component_under_test.add(datum('02.01.2017'), '2kategorie', '2name', 1.54)
        component_under_test.add(datum('03.01.2017'), '1kategorie', '1name', 1.54)

        assert component_under_test.content.Datum[0] == datum('01.01.2017')

        component_under_test.edit(0, datum('15.01.2017'), 'some other kategorie', 'some other name', 2.65)

        assert len(component_under_test.content) == 3
        assert set(component_under_test.content.Name) == set(['1name', '2name', 'some other name'])
        assert set(component_under_test.content.Datum) == set([datum('02.01.2017'), datum('03.01.2017'), datum('15.01.2017')])

        changed_row = component_under_test.content[component_under_test.content.Datum == datum('15.01.2017')]
        changed_row.reset_index(drop=True, inplace=True)
        assert changed_row.Name[0] == 'some other name'
        assert changed_row.Kategorie[0] == 'some other kategorie'
        assert changed_row.Wert[0] == 2.65

    def test_get_single_einzelbuchung(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), '1kategorie', '1name', 1.54)

        result = component_under_test.get(0)

        assert result['index'] == 0
        assert result['Datum'] == date.today()
        assert result['Name'] == '1name'
        assert result['Kategorie'] == '1kategorie'
        assert result['Wert'] == 1.54

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2012'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01.01.2013'), '1kategorie', '1name', 1)

        assert component_under_test.get_all().Datum[0].year == 2011
        assert component_under_test.get_all().Datum[1].year == 2012
        assert component_under_test.get_all().Datum[2].year == 2013

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum_Kategorie(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01.01.2011'), '3kategorie', '1name', 1)
        component_under_test.add(datum('01.01.2011'), '2kategorie', '1name', 1)

        assert component_under_test.get_all().Kategorie[0] == '1kategorie'
        assert component_under_test.get_all().Kategorie[1] == '2kategorie'
        assert component_under_test.get_all().Kategorie[2] == '3kategorie'

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum_Kategorie_Name(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01.01.2011'), '1kategorie', '3name', 1)
        component_under_test.add(datum('01.01.2011'), '1kategorie', '2name', 1)

        assert component_under_test.get_all().Name[0] == '1name'
        assert component_under_test.get_all().Name[1] == '2name'
        assert component_under_test.get_all().Name[2] == '3name'

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum_Kategorie_Name_Wert(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 10)
        component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 5)

        assert component_under_test.get_all().Wert[0] == 1
        assert component_under_test.get_all().Wert[1] == 5
        assert component_under_test.get_all().Wert[2] == 10


    def test_edit_einzelbuchung_shouldRefreshSortingOfEinzelbuchungen(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2012'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01.01.2013'), '1kategorie', '1name', 1)

        component_under_test.edit(0, datum('01.01.2020'), '1kategorie', '1name', 1)

        assert component_under_test.get_all().Datum[0].year == 2012
        assert component_under_test.get_all().Datum[1].year == 2013
        assert component_under_test.get_all().Datum[2].year == 2020

    def test_anzahl_withEmptyDB_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()

        assert component_under_test.anzahl() == 0

    def test_anzahl_withOneEntry_shouldReturnOne(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2012'), '1kategorie', '1name', 1)

        assert component_under_test.anzahl() == 1


class gesamtausgaben_jahr(unittest.TestCase):

    def test_getJahresausgabenNachKategorieProzentual_withEmptyDB_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert result == {}

    def test_getJahresausgabenNachKategorieProzentual_withEinnahme_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2015'), 'kategorie 1', 'some name', 10)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert result == {}


    def test_getJahresausgabenNachKategorieProzentual_withAusgabeAußerhalbDesJahres_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2014'), 'kategorie 1', 'some name', -10)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert result == {}

    def test_getJahresausgabenNachKategorieProzentual_withOneEntry_shouldReturnKategorieWith100Percent(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2015'), 'kategorie 1', 'some name', -10)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert set(result.keys()) == set(['kategorie 1'])
        assert  result['kategorie 1'] == 100.00

    def test_getJahresausgabenNachKategorieProzentual_withTwoEntrys_shouldReturnResult(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2015'), 'kategorie 1', 'some name', -7.5)
        component_under_test.add(datum('01.01.2015'), 'kategorie 2', 'some name', -2.5)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert set(result.keys()) == set(['kategorie 1', 'kategorie 2'])
        assert  result['kategorie 1'] == 75.00
        assert  result['kategorie 2'] == 25.00

    def teste_durchschnittliche_ausgaben_pro_monat_withEmptyDB_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {}

    def teste_durchschnittliche_ausgaben_pro_monat_withNonmatchingYear_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('10.10.2010'), 'K', '', -10)

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {}

    def teste_durchschnittliche_ausgaben_pro_monat_withEinnahme_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('10.10.2011'), 'K', '', 10)

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {}

    def teste_durchschnittliche_ausgaben_pro_monat_withMatchingAndClosedYear_shouldReturnMonthlyPart(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('10.10.2010'), 'K', '', -10)
        component_under_test.add(datum('10.10.2011'), 'K', '', -12)

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {'K':"1.00"}

    def teste_durchschnittliche_ausgaben_pro_monat_shouldReturnMonthlyPart(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('10.10.2010'), 'K', '', -10)
        component_under_test.add(datum('10.10.2011'), 'B', '', -12)
        component_under_test.add(datum('10.10.2011'), 'A', '', -24)

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {'A':"2.00", 'B':'1.00'}

    def teste_durchschnittliche_ausgaben_pro_monat_mitAngefangenemJahr_sollteDurchAnzahlDerEntsprechendenMonateTeilen(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('10.8.2011'), 'B', '', -10)

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == { 'B':'2.00'}

    def teste_durchschnittliche_ausgaben_pro_monat_mitNurLetztemMonat_sollteAusgabenDurchEinsTeilen(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('10.8.2011'), 'A', '', -10)

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011, today=datum('10.9.2011')) == {'A':'10.00'}

    def teste_durchschnittliche_ausgaben_pro_monat_mitNurHeute_sollteAktuellenMonatIgnorieren(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), 'A', '', -10)

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(date.today().year) == {}


class einzelbuchungs_selector(unittest.TestCase):

    def test_inject_zeroes_for_year_and_kategories_shouldInjectZeroes(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.02.2017'), 'kat1', '', 5,)
        component_under_test.add(datum('01.02.2017'), 'kat2', '', 5,)
        result = component_under_test.select().inject_zeroes_for_year_and_kategories(2017).raw_table()
        assert len(result) == 26
        assert datum('01.01.2017') in set(result.Datum)
        assert datum('01.12.2017') in set(result.Datum)
        assert result.Wert.sum() == 10
        assert set(['kat1', 'kat2']) == set(result.Kategorie)

    def test_sum_kategorien_monthly(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.02.2017'), 'kat1', '', 5,)
        component_under_test.add(datum('01.02.2017'), 'kat2', '', 10,)
        result = component_under_test.select().sum_kategorien_monthly()
        assert len(result) == 1
        assert len(result[2]) == 2
        assert result[2]['kat1'] == '5.00'
        assert result[2]['kat2'] == '10.00'

    def test_inject_zeroes_for_year_and_kategories_wothNoValues_shouldInjectZeroes(self):
        component_under_test = Einzelbuchungen()
        assert component_under_test.select().inject_zeroes_for_year_and_kategories(2017).sum() == 0


    def test_injectZeros_shouldInjectZeroes(self):
        component_under_test = Einzelbuchungen()
        select = component_under_test.select()

        assert len(select.content) == 0

        select = select.inject_zeros_for_year(2017)
        assert len(select.content) == 12
        assert select.content.loc[0].Datum == datum('01.01.2017')
        assert select.content.loc[11].Datum == datum('01.12.2017')
        assert select.content.Wert.sum() == 0

    def test_sumMonthly_withUniqueMonths(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2017'), '', '', 20,)
        component_under_test.add(datum('01.02.2017'), '', '', 10,)

        result = component_under_test.select().sum_monthly()

        assert result == ['20.00', '10.00']

    def test_sumMonthly_withDuplicatedMonths_shouldSumValues(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.02.2017'), '', '', 5,)
        component_under_test.add(datum('01.01.2017'), '', '', 20,)
        component_under_test.add(datum('01.02.2017'), '', '', 10,)

        result = component_under_test.select().sum_monthly()

        assert result == ['20.00', '15.00']

    def test_sum_withEmptyDB_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()
        assert component_under_test.select().sum() == 0

    def test_sum_withBuchung_shouldReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2010'), '', '', 10)

        assert component_under_test.select().sum() == 10

    def test_filterYear_withNonMatchingYear_shouldRemoveItem(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2010'), '', '', 10)

        assert component_under_test.select().select_year(2011).sum() == 0

    def test_filterYear_withMatchingYear_shoudReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', 10)

        assert component_under_test.select().select_year(2011).sum() == 10

    def test_einnahmen_withEinnahme_shoudReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', 10)

        assert component_under_test.select().select_einnahmen().select_year(2011).sum() == 10

    def test_einnahmen_withAusgabe_shoudReturnZero(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', -10)

        assert component_under_test.select().select_einnahmen().select_year(2011).sum() == 0

    def test_ausgaben_withEinnahme_shoudReturnZero(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', 10)

        assert component_under_test.select().select_ausgaben().select_year(2011).sum() == 0

    def test_ausgaben_withAusgabe_shoudReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', -10)

        assert component_under_test.select().select_ausgaben().select_year(2011).sum() == -10

    def test_select_withMonthSelection_andMatchingMonth_shouldReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', -10)

        assert component_under_test.select().select_month(1).sum() == -10

    def test_select_withMonthSelection_andEmptyDB_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()

        assert component_under_test.select().select_month(1).sum() == 0

    def test_select_withMonthSelection_andNonMatchingMonth_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', -10)

        assert component_under_test.select().select_month(2).sum() == 0

    def test_select_withThisMonthSelection_andMatchingMonth_shouldReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), '', '', -10)

        assert component_under_test.select().select_aktueller_monat().sum() == -10

    def test_select_withThisMonthSelection_andNonMatchingDate_shouldReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('20.01.1990'), '', '', -10)

        assert component_under_test.select().select_aktueller_monat().sum() == 0

    def test_group_by_kategorie_withEmptyDB_shouldReturnEmptyTable(self):
        component_under_test = Einzelbuchungen()

        assert component_under_test.select().group_by_kategorie().empty

    def test_group_by_kategorie_shouldGroupValues(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('20.01.1990'), 'A', '', -10)
        component_under_test.add(datum('20.01.1990'), 'A', '', -10)
        component_under_test.add(datum('20.01.1990'), 'B', '', 8)


        assert component_under_test.select().group_by_kategorie().Wert.tolist() == [-20, 8]
        assert component_under_test.select().group_by_kategorie().index.tolist() == ['A', 'B']
