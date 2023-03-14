from datetime import date

from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen


def test__get_jahresausgaben_nach_kategorie_prozentual__with_empty_db__should_return_empty_dict():
    component_under_test = Einzelbuchungen()

    result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

    assert result == {}


def test__get_jahresausgaben_nach_kategorie_prozentual__with_einnahme__should_return_empty_dict():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2015'), 'kategorie 1', 'some name', 10)

    result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

    assert result == {}


def test__get_jahresausgaben_nach_kategorie_prozentual__with_ausgabe_ausserhalb_des_jahres__should_return_empty_dict():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2014'), 'kategorie 1', 'some name', -10)

    result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

    assert result == {}


def test__get_jahresausgaben_nach_kategorie_prozentual__with_one_entry__should_return_kategorie_with_100_percent():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2015'), 'kategorie 1', 'some name', -10)

    result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

    assert set(result.keys()) == {'kategorie 1'}
    assert result['kategorie 1'] == 100.00


def test_getJahresausgabenNachKategorieProzentual_withTwoEntrys_shouldReturnResult():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2015'), 'kategorie 1', 'some name', -7.5)
    component_under_test.add(datum('01.01.2015'), 'kategorie 2', 'some name', -2.5)

    result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

    assert set(result.keys()) == {'kategorie 1', 'kategorie 2'}
    assert result['kategorie 1'] == 75.00
    assert result['kategorie 2'] == 25.00


def teste_durchschnittliche_ausgaben_pro_monat_withEmptyDB_shouldReturnEmptyDict():
    component_under_test = Einzelbuchungen()

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {}


def teste_durchschnittliche_ausgaben_pro_monat_withNonmatchingYear_shouldReturnEmptyDict():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.10.2010'), 'K', '', -10)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {}


def teste_durchschnittliche_ausgaben_pro_monat_withEinnahme_shouldReturnEmptyDict():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.10.2011'), 'K', '', 10)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {}


def teste_durchschnittliche_ausgaben_pro_monat_withMatchingAndClosedYear_shouldReturnMonthlyPart():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.10.2010'), 'K', '', -10)
    component_under_test.add(datum('10.10.2011'), 'K', '', -12)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {'K': "1.00"}


def teste_durchschnittliche_ausgaben_pro_monat_shouldReturnMonthlyPart():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.10.2010'), 'K', '', -10)
    component_under_test.add(datum('10.10.2011'), 'B', '', -12)
    component_under_test.add(datum('10.10.2011'), 'A', '', -24)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {'A': "2.00", 'B': '1.00'}


def teste_durchschnittliche_ausgaben_pro_monat_mitAngefangenemJahr_sollteDurchAnzahlDerEntsprechendenMonateTeilen():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.8.2011'), 'B', '', -10)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {'B':'2.00'}


def teste_durchschnittliche_ausgaben_pro_monat_mitNurLetztemMonat_sollteAusgabenDurchEinsTeilen():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.8.2011'), 'A', '', -10)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011, today=datum('10.9.2011')) == {'A':'10.00'}


def teste_durchschnittliche_ausgaben_pro_monat_mitNurHeute_sollteAktuellenMonatIgnorieren():
    component_under_test = Einzelbuchungen()
    component_under_test.add(date.today(), 'A', '', -10)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(date.today().year) == {}
