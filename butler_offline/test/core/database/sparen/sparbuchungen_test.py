from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.core.database import extract_index, extract_name_column


def test_get_static_content_should_filter_dynamic_content():
    component_under_test = Sparbuchungen()

    component_under_test.add(datum('01.01.2012'), '1name', 1, '1typ', '1konto')
    component_under_test.add(datum('02.02.2013'), '2name', 2, '2typ', '2konto', dynamisch=True)

    static_content = component_under_test.get_static_content()

    assert len(static_content) == 1
    assert static_content.Datum[0] == datum('01.01.2012')
    assert static_content.Typ[0] == '1typ'
    assert static_content.Name[0] == '1name'
    assert static_content.Wert[0] == 1
    assert static_content.Konto[0] == '1konto'
    assert 'Dynamisch' not in static_content.columns


def test_add_should_add():
    component_under_test = Sparbuchungen()

    component_under_test.add(datum('01.01.2012'), '1name', 1, '1typ', '1konto', dynamisch=True)

    assert len(component_under_test.content) == 1
    assert component_under_test.content.Datum[0] == datum('01.01.2012')
    assert component_under_test.content.Typ[0] == '1typ'
    assert component_under_test.content.Name[0] == '1name'
    assert component_under_test.content.Wert[0] == 1
    assert component_under_test.content.Konto[0] == '1konto'
    assert component_under_test.content.Dynamisch[0]


def test_edit_should_edit():
    component_under_test = Sparbuchungen()

    component_under_test.add(datum('04.04.2010'), '0name', 0, '0typ', '0konto', dynamisch=True)
    component_under_test.add(datum('01.01.2011'), '1name', 1, '1typ', '1konto', dynamisch=True)
    component_under_test.add(datum('02.02.2012'), '2name', 2, '2typ', '2konto', dynamisch=True)

    assert len(component_under_test.content) == 3
    element_before = component_under_test.get(1)
    assert element_before == {
        'Datum': datum('01.01.2011'),
        'Dynamisch': True,
        'Konto': '1konto',
        'Name': '1name',
        'Typ': '1typ',
        'Wert': 1,
        'index': 1
    }

    component_under_test.edit(1, datum('03.03.2011'), '3name', 3, '3typ', '3konto')

    assert len(component_under_test.content) == 3
    element_after = component_under_test.get(1)
    assert element_after == {
        'Datum': datum('03.03.2011'),
        'Dynamisch': True,
        'Konto': '3konto',
        'Name': '3name',
        'Typ': '3typ',
        'Wert': 3,
        'index': 1
    }


def test_add_should_sort_and_drop_index():
    component_under_test = Sparbuchungen()

    component_under_test.add(datum('04.04.2020'), 'name1', 0, '0typ', '0konto', dynamisch=True)
    component_under_test.add(datum('04.04.2010'), 'name2', 0, '0typ', '0konto', dynamisch=True)

    assert extract_name_column(component_under_test) == ['name2', 'name1']
    assert extract_index(component_under_test) == [0, 1]


def test_edit_should_sort_and_drop_index():
    component_under_test = Sparbuchungen()#

    component_under_test.add(datum('04.04.2010'), 'name1', 0, '0typ', '0konto', dynamisch=True)
    component_under_test.add(datum('04.04.2020'), 'name2', 0, '0typ', '0konto', dynamisch=True)

    component_under_test.edit(1, datum('04.04.2000'), 'name2', 0, '0typ', '0konto')

    assert extract_name_column(component_under_test) == ['name2', 'name1']
    assert extract_index(component_under_test) == [0, 1]


def test_get_dynamische_einzelbuchungen():
    component_under_test = Sparbuchungen()

    component_under_test.add(datum('01.01.2011'), '1name', 1, Sparbuchungen.TYP_AUSSCHUETTUNG, '1konto')
    component_under_test.add(datum('02.02.2012'), '2name', 2, Sparbuchungen.TYP_MANUELLER_AUFTRAG, '2konto')
    component_under_test.add(datum('03.03.2013'), '3name', -3, Sparbuchungen.TYP_MANUELLER_AUFTRAG, '3konto')
    component_under_test.add(datum('04.04.2014'), '4name', 4, Sparbuchungen.TYP_ZINSEN, '3konto')

    result = component_under_test.get_dynamische_einzelbuchungen()

    assert len(result) == 3
    assert set(result.columns) == set(Einzelbuchungen.TABLE_HEADER)

    assert result.Datum[0] == datum('01.01.2011')
    assert result.Name[0] == '1name'
    assert result.Kategorie[0] == Sparbuchungen.TYP_AUSSCHUETTUNG
    assert result.Wert[0] == 1
    assert result.Dynamisch[0]
    assert result.Tags[0] == []

    assert result.Datum[1] == datum('02.02.2012')
    assert result.Name[1] == '2name'
    assert result.Kategorie[1] == 'Sparen'
    assert result.Wert[1] == -2
    assert result.Dynamisch[1]
    assert result.Tags[1] == []

    assert result.Datum[2] == datum('03.03.2013')
    assert result.Name[2] == '3name'
    assert result.Kategorie[2] == 'Sparen'
    assert result.Wert[2] == 3
    assert result.Dynamisch[2]
    assert result.Tags[2] == []


def test_get_kontostand_fuer():
    component_under_test = Sparbuchungen()

    component_under_test.add(datum('01.01.2011'), '1name', 1, Sparbuchungen.TYP_AUSSCHUETTUNG, 'konto')
    component_under_test.add(datum('02.02.2012'), '2name', 200, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('03.03.2013'), '3name', -50, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('03.03.2013'), '3name', -3, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'anderes_konto')
    component_under_test.add(datum('04.04.2014'), '4name', 10, Sparbuchungen.TYP_ZINSEN, 'konto')

    assert component_under_test.get_kontostand_fuer('konto') == 160


def test_get_aufbuchungen_fuer():
    component_under_test = Sparbuchungen()

    component_under_test.add(datum('01.01.2011'), '1name', 1, Sparbuchungen.TYP_AUSSCHUETTUNG, 'konto')
    component_under_test.add(datum('02.02.2012'), '2name', 200, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('03.03.2013'), '3name', -50, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('03.03.2013'), '3name', -3, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'anderes_konto')
    component_under_test.add(datum('04.04.2014'), '4name', 10, Sparbuchungen.TYP_ZINSEN, 'konto')

    assert component_under_test.get_aufbuchungen_fuer('konto') == 150


def test_select_year():
    component_under_test = Sparbuchungen()

    component_under_test.add(datum('01.01.2010'), '1name', 1, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('01.01.2011'), '1name', 1, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('01.01.2012'), '1name', 1, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('01.01.2013'), '1name', 33, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('01.01.2014'), '1name', 1, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')

    assert component_under_test.select_year(2013).get_aufbuchungen_fuer('konto') == 33


def test_select_max_year():
    component_under_test = Sparbuchungen()

    component_under_test.add(datum('01.01.2010'), '1name', 1, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('01.01.2011'), '1name', 1, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('01.01.2012'), '1name', 1, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('01.01.2013'), '1name', 33, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')
    component_under_test.add(datum('01.01.2014'), '1name', 1, Sparbuchungen.TYP_MANUELLER_AUFTRAG, 'konto')

    assert component_under_test.select_max_year(2013).get_aufbuchungen_fuer('konto') == 36


