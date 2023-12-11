from datetime import date

from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.viewcore.converter import datum_from_german as datum


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


def test_get_jahresausgaben_nach_kategorie_prozentual_with_two_entrys_should_return_result():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2015'), 'kategorie 1', 'some name', -7.5)
    component_under_test.add(datum('01.01.2015'), 'kategorie 2', 'some name', -2.5)

    result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

    assert set(result.keys()) == {'kategorie 1', 'kategorie 2'}
    assert result['kategorie 1'] == 75.00
    assert result['kategorie 2'] == 25.00


def teste_durchschnittliche_ausgaben_pro_monat_with_empty_database_should_return_empty_dict():
    component_under_test = Einzelbuchungen()

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {}


def teste_durchschnittliche_ausgaben_pro_monat_with_non_matching_year_should_return_empty_dict():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.10.2010'), 'K', '', -10)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {}


def teste_durchschnittliche_ausgaben_pro_monat_with_einnahme_should_return_empty_dict():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.10.2011'), 'K', '', 10)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {}


def teste_durchschnittliche_ausgaben_pro_monat_with_matching_and_closed_year_should_return_monthly_part():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.10.2010'), 'K', '', -10)
    component_under_test.add(datum('10.10.2011'), 'K', '', -12)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {'K': "1.00"}


def teste_durchschnittliche_ausgaben_pro_monat_should_return_monthly_part():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.10.2010'), 'K', '', -10)
    component_under_test.add(datum('10.10.2011'), 'B', '', -12)
    component_under_test.add(datum('10.10.2011'), 'A', '', -24)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {'A': "2.00", 'B': '1.00'}


def teste_durchschnittl_ausgaben_pro_monat_mit_angefangenem_jahr_sollte_durch_anzahl_der_entsprechenden_monate_teilen():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.8.2011'), 'B', '', -10)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011) == {'B': '2.00'}


def teste_durchschnittliche_ausgaben_pro_monat_mit_nur_letztem_monat_sollte_ausgaben_durch_eins_teilen():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('10.8.2011'), 'A', '', -10)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(2011, today=datum('10.9.2011')) == {'A': '10.00'}


def teste_durchschnittliche_ausgaben_pro_monat_mit_nur_heute_sollte_aktuellen_monat_ignorieren():
    component_under_test = Einzelbuchungen()
    component_under_test.add(date.today(), 'A', '', -10)

    assert component_under_test.durchschnittliche_ausgaben_pro_monat(date.today().year) == {}
