from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen


def test_schliesse_kategorien_aus_ausgaben():
    component_under_test = Einzelbuchungen()
    component_under_test.ausgeschlossene_kategorien = {'NeinEins'}
    component_under_test.add(datum('20.01.1990'), 'JaEins', 'SomeTitle', -10)
    component_under_test.add(datum('20.01.1990'), 'NeinEins', 'SomeTitle', -10)
    component_under_test.add(datum('20.01.1990'), 'JaZwei', 'SomeTitle', -10)

    assert component_under_test.get_kategorien_ausgaben(hide_ausgeschlossene_kategorien=True) == {'JaEins',
                                                                                                  'JaZwei'}


def test_schliesse_kategorien_aus_einnahmen():
    component_under_test = Einzelbuchungen()
    component_under_test.ausgeschlossene_kategorien = {'NeinEins'}
    component_under_test.add(datum('20.01.1990'), 'JaEins', 'SomeTitle', 10)
    component_under_test.add(datum('20.01.1990'), 'NeinEins', 'SomeTitle', 10)
    component_under_test.add(datum('20.01.1990'), 'JaZwei', 'SomeTitle', 10)

    assert component_under_test.get_kategorien_einnahmen(hide_ausgeschlossene_kategorien=True) == {'JaEins',
                                                                                                   'JaZwei'}


def test_schliesse_kategorien_aus_allen_buchungen():
    component_under_test = Einzelbuchungen()
    component_under_test.ausgeschlossene_kategorien = {'NeinEins', 'NeinZwei'}
    component_under_test.add(datum('20.01.1990'), 'JaEins', 'SomeTitle', 10)
    component_under_test.add(datum('20.01.1990'), 'NeinEins', 'SomeTitle', 10)
    component_under_test.add(datum('20.01.1990'), 'NeinZwei', 'SomeTitle', -10)
    component_under_test.add(datum('20.01.1990'), 'JaZwei', 'SomeTitle', -10)

    assert component_under_test.get_alle_kategorien(hide_ausgeschlossene_kategorien=True) == {'JaEins', 'JaZwei'}
