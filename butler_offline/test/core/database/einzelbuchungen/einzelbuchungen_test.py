from datetime import date

from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.core.database import extract_index, extract_name_column


def test_add_should_taint():
    component_under_test = Einzelbuchungen()
    assert component_under_test.taint_number() == 0
    component_under_test.add(
        datum('1.1.2010'),
        'some kategorie',
        'some name',
        1.23)
    assert component_under_test.taint_number() == 1


def test_edit_should_taint():
    component_under_test = Einzelbuchungen()
    component_under_test.add(
        datum('1.1.2010'),
        'some kategorie',
        'some name',
        1.23)
    assert component_under_test.taint_number() == 1
    component_under_test.edit(
        0,
        datum('2.1.2010'),
        'some other kategorie',
        'some other name',
        2.34)
    assert component_under_test.taint_number() == 2


def test_add_should_sort_and_drop_index():
    component_under_test = Einzelbuchungen()
    component_under_test.add(
        datum('1.1.2020'),
        'kategorie1',
        'name1',
        1.23)
    component_under_test.add(
        datum('1.1.2010'),
        'kategorie2',
        'name2',
        1.23)

    assert extract_name_column(component_under_test) == ['name2', 'name1']
    assert extract_index(component_under_test) == [0, 1]


def test_edit_should_sort_and_drop_index():
    component_under_test = Einzelbuchungen()
    component_under_test.add(
        datum('1.1.2010'),
        'kategorie1',
        'name1',
        1.23)
    component_under_test.add(
        datum('1.1.2020'),
        'kategorie2',
        'name2',
        1.23)

    component_under_test.edit(
        1,
        datum('1.1.2000'),
        'kategorie2',
        'name2',
        1.23)

    assert extract_name_column(component_under_test) == ['name2', 'name1']
    assert extract_index(component_under_test) == [0, 1]


def test_delete_should_taint():
    component_under_test = Einzelbuchungen()
    component_under_test.add(
        datum('1.1.2010'),
        date.today(),
        'some kategorie',
        'some name',
        1.23)
    assert component_under_test.taint_number() == 1
    component_under_test.delete(0)
    assert component_under_test.taint_number() == 2


def test_add():
    component_under_test = Einzelbuchungen()
    component_under_test.add(date.today(), 'some kategorie', 'some name', 1.54)

    assert len(component_under_test.content) == 1
    assert component_under_test.content.Datum[0] == date.today()
    assert component_under_test.content.Name[0] == 'some name'
    assert component_under_test.content.Kategorie[0] == 'some kategorie'
    assert component_under_test.content.Wert[0] == 1.54
    assert component_under_test.content.Tags[0] == []


def test_aendere__bei_einziger_einzelbuchung():
    component_under_test = Einzelbuchungen()
    component_under_test.add(date.today(), 'some kategorie', 'some name', 1.54)
    component_under_test.edit(0, date.today(), 'some other kategorie', 'some other name', 2.65)

    assert component_under_test.select().count() == 1
    assert component_under_test.content.Datum[0] == date.today()
    assert component_under_test.content.Name[0] == 'some other name'
    assert component_under_test.content.Kategorie[0] == 'some other kategorie'
    assert component_under_test.content.Wert[0] == 2.65


def test_aendere__bei_voller_datenbank():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2017'), '3kategorie', '3name', 1.54)
    component_under_test.add(datum('02.01.2017'), '2kategorie', '2name', 1.54)
    component_under_test.add(datum('03.01.2017'), '1kategorie', '1name', 1.54)

    assert component_under_test.content.Datum[0] == datum('01.01.2017')

    component_under_test.edit(0, datum('15.01.2017'), 'some other kategorie', 'some other name', 2.65)

    assert component_under_test.select().count() == 3
    assert set(component_under_test.content.Name) == {'1name', '2name', 'some other name'}
    assert set(component_under_test.content.Datum) == {datum('02.01.2017'), datum('03.01.2017'),
                                                       datum('15.01.2017')}

    changed_row = component_under_test.content[component_under_test.content.Datum == datum('15.01.2017')]
    changed_row.reset_index(drop=True, inplace=True)
    assert changed_row.Name[0] == 'some other name'
    assert changed_row.Kategorie[0] == 'some other kategorie'
    assert changed_row.Wert[0] == 2.65


def test_get_single_einzelbuchung():
    component_under_test = Einzelbuchungen()
    component_under_test.add(date.today(), '1kategorie', '1name', 1.54)

    result = component_under_test.get(0)

    assert result['index'] == 0
    assert result['Datum'] == date.today()
    assert result['Name'] == '1name'
    assert result['Kategorie'] == '1kategorie'
    assert result['Wert'] == 1.54


def test_get_einzelbuchungen_should_return_list_sorted_by_datum():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2012'), '1kategorie', '1name', 1)
    component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 1)
    component_under_test.add(datum('01.01.2013'), '1kategorie', '1name', 1)

    assert component_under_test.get_all().Datum[0].year == 2011
    assert component_under_test.get_all().Datum[1].year == 2012
    assert component_under_test.get_all().Datum[2].year == 2013


def test_get_einzelbuchungen__should_return_list_sorted_by_datum_kategorie():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 1)
    component_under_test.add(datum('01.01.2011'), '3kategorie', '1name', 1)
    component_under_test.add(datum('01.01.2011'), '2kategorie', '1name', 1)

    assert component_under_test.get_all().Kategorie[0] == '1kategorie'
    assert component_under_test.get_all().Kategorie[1] == '2kategorie'
    assert component_under_test.get_all().Kategorie[2] == '3kategorie'


def test_get_einzelbuchungen_should_return_list_sorted_by_datum_kategorie_name():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 1)
    component_under_test.add(datum('01.01.2011'), '1kategorie', '3name', 1)
    component_under_test.add(datum('01.01.2011'), '1kategorie', '2name', 1)

    assert component_under_test.get_all().Name[0] == '1name'
    assert component_under_test.get_all().Name[1] == '2name'
    assert component_under_test.get_all().Name[2] == '3name'


def test_get_einzelbuchungen_should_return_list_sorted_by_datum_kategorie_name_wert():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 1)
    component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 10)
    component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 5)

    assert component_under_test.get_all().Wert[0] == 1
    assert component_under_test.get_all().Wert[1] == 5
    assert component_under_test.get_all().Wert[2] == 10


def test_edit_einzelbuchung_should_refresh_sorting_of_einzelbuchungen():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2012'), '1kategorie', '1name', 1)
    component_under_test.add(datum('01.01.2011'), '1kategorie', '1name', 1)
    component_under_test.add(datum('01.01.2013'), '1kategorie', '1name', 1)

    component_under_test.edit(0, datum('01.01.2020'), '1kategorie', '1name', 1)

    assert component_under_test.get_all().Datum[0].year == 2012
    assert component_under_test.get_all().Datum[1].year == 2013
    assert component_under_test.get_all().Datum[2].year == 2020


def test_get_static_content_should_filter_dynamic_content():
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


def test_rename_should_rename():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2012'), '1kategorie', '1name', 1)
    component_under_test.add(datum('01.01.2013'), '2kategorie', '2name', 2)
    component_under_test.add(datum('01.01.2014'), '3kategorie', '3name', 3)

    element1 = {'Datum': datum('01.01.2012'),
                'Dynamisch': False,
                'Kategorie': '1kategorie',
                'Name': '1name',
                'Tags': [],
                'Wert': 1,
                'index': 0}
    element2 = {'Datum': datum('01.01.2013'),
                'Dynamisch': False,
                'Kategorie': '2kategorie',
                'Name': '2name',
                'Tags': [],
                'Wert': 2,
                'index': 1}
    element3 = {'Datum': datum('01.01.2014'),
                'Dynamisch': False,
                'Kategorie': '3kategorie',
                'Name': '3name',
                'Tags': [],
                'Wert': 3,
                'index': 2}
    assert component_under_test.select().to_list() == [element1,
                                                       element2,
                                                       element3]
    component_under_test.rename_kategorie(alter_name='2kategorie', neuer_name='4kategorie')

    assert component_under_test.select().to_list() == [element1,
                                                       {'Datum': datum('01.01.2013'),
                                                        'Dynamisch': False,
                                                        'Kategorie': '4kategorie',
                                                        'Name': '2name',
                                                        'Tags': [],
                                                        'Wert': 2,
                                                        'index': 1},
                                                       element3]
    assert component_under_test.tainted


def test_rename_should_sort():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2012'), '1kategorie', '1name', 1)
    component_under_test.add(datum('01.01.2012'), '2kategorie', '2name', 2)

    element1 = {'Datum': datum('01.01.2012'),
                'Dynamisch': False,
                'Kategorie': '1kategorie',
                'Name': '1name',
                'Tags': [],
                'Wert': 1,
                'index': 0}
    element2 = {'Datum': datum('01.01.2012'),
                'Dynamisch': False,
                'Kategorie': '2kategorie',
                'Name': '2name',
                'Tags': [],
                'Wert': 2,
                'index': 1}
    assert component_under_test.select().to_list() == [element1,
                                                       element2]
    component_under_test.rename_kategorie(alter_name='2kategorie', neuer_name='0kategorie')

    assert component_under_test.select().to_list() == [{'Datum': datum('01.01.2012'),
                                                        'Dynamisch': False,
                                                        'Kategorie': '0kategorie',
                                                        'Name': '2name',
                                                        'Tags': [],
                                                        'Wert': 2,
                                                        'index': 0},
                                                       element1 | index(1)
                                                       ]
    assert component_under_test.tainted


def index(new_index: int):
    return {'index': new_index}
