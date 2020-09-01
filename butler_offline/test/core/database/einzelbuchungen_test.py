'''
Created on 11.08.2017

@author: sebastian
'''
from datetime import date
import unittest

from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen


class EinzelbuchungenTest(unittest.TestCase):

    def test_add_shouldTaint(self):
        component_under_test = Einzelbuchungen()
        assert component_under_test.taint_number() == 0
        component_under_test.add(
            datum('1.1.2010'),
            'some kategorie',
            'some name',
            1.23)
        assert component_under_test.taint_number() == 1

    def test_edit_shouldTaint(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(
            datum('1.1.2010'),
            'some kategorie',
            'some name',
            1.23)
        component_under_test.de_taint()
        assert component_under_test.taint_number() == 0
        component_under_test.edit(
            0,
            datum('2.1.2010'),
            'some other kategorie',
            'some other name',
            2.34)
        assert component_under_test.taint_number() == 1

    def test_delete_shouldTaint(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(
            datum('1.1.2010'),
            date.today(),
            'some kategorie',
            'some name',
            1.23)
        component_under_test.de_taint()
        assert component_under_test.taint_number() == 0
        component_under_test.delete(0)
        assert component_under_test.taint_number() == 1


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

    def test_get_static_content_should_filter_dynamic_content(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2012'), '1kategorie', '1name', 1)
        component_under_test.add(datum('02.02.2013'), '2kategorie', '2name', 2, dynamisch=True)

        static_content = component_under_test.get_static_content()

        assert len(static_content) == 1
        assert static_content.Datum[0] == datum('01.01.2012')
        assert static_content.Kategorie[0] == '1kategorie'
        assert static_content.Name[0] == '1name'
        assert static_content.Wert[0] == 1
        assert 'Dynamisch' not in static_content.columns


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

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {'B':'2.00'}

    def teste_durchschnittliche_ausgaben_pro_monat_mitNurLetztemMonat_sollteAusgabenDurchEinsTeilen(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('10.8.2011'), 'A', '', -10)

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011, today=datum('10.9.2011')) == {'A':'10.00'}

    def teste_durchschnittliche_ausgaben_pro_monat_mitNurHeute_sollteAktuellenMonatIgnorieren(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), 'A', '', -10)

        assert component_under_test.durchschnittliche_ausgaben_pro_monat(date.today().year) == {}


class kategorien_selector(unittest.TestCase):

    def test_schliesse_kategorien_aus_ausgaben(self):
        component_under_test = Einzelbuchungen()
        component_under_test.ausgeschlossene_kategorien = set(['NeinEins'])
        component_under_test.add(datum('20.01.1990'), 'JaEins', 'SomeTitle', -10)
        component_under_test.add(datum('20.01.1990'), 'NeinEins', 'SomeTitle', -10)
        component_under_test.add(datum('20.01.1990'), 'JaZwei', 'SomeTitle', -10)

        assert component_under_test.get_kategorien_ausgaben(hide_ausgeschlossene_kategorien=True) == set(['JaEins', 'JaZwei'])


    def test_schliesse_kategorien_aus_einnahmen(self):
        component_under_test = Einzelbuchungen()
        component_under_test.ausgeschlossene_kategorien = set(['NeinEins'])
        component_under_test.add(datum('20.01.1990'), 'JaEins', 'SomeTitle', 10)
        component_under_test.add(datum('20.01.1990'), 'NeinEins', 'SomeTitle', 10)
        component_under_test.add(datum('20.01.1990'), 'JaZwei', 'SomeTitle', 10)

        assert component_under_test.get_kategorien_einnahmen(hide_ausgeschlossene_kategorien=True) == set(['JaEins', 'JaZwei'])



    def test_schliesse_kategorien_aus_allen_buchungen(self):
        component_under_test = Einzelbuchungen()
        component_under_test.ausgeschlossene_kategorien = set(['NeinEins', 'NeinZwei'])
        component_under_test.add(datum('20.01.1990'), 'JaEins', 'SomeTitle', 10)
        component_under_test.add(datum('20.01.1990'), 'NeinEins', 'SomeTitle', 10)
        component_under_test.add(datum('20.01.1990'), 'NeinZwei', 'SomeTitle', -10)
        component_under_test.add(datum('20.01.1990'), 'JaZwei', 'SomeTitle', -10)

        assert component_under_test.get_alle_kategorien(hide_ausgeschlossene_kategorien=True) == set(['JaEins', 'JaZwei'])
