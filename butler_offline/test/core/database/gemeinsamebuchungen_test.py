from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen


def test_add_should_taint():
    component_under_test = Gemeinsamebuchungen()
    assert component_under_test.taint_number() == 0
    component_under_test.add(
        datum('1.1.2010'),
        'some kategorie',
        'some name',
        1.23,
        'sebastian')
    assert component_under_test.taint_number() == 1


def test_edit_should_taint():
    component_under_test = Gemeinsamebuchungen()
    component_under_test.add(
        datum('1.1.2010'),
        'some kategorie',
        'some name',
        1.23,
        'sebastian')
    assert component_under_test.taint_number() == 1
    component_under_test.edit(
        0,
        datum('2.1.2010'),
        'some other kategorie',
        'some other name',
        2.34,
        'sebastian')
    assert component_under_test.taint_number() == 2


def test_edit_should_edit():
    component_under_test = Gemeinsamebuchungen()
    component_under_test.add(
        datum('1.1.2011'),
        'yyName',
        'yyKategorie',
        1.23,
        'sebastian')
    assert component_under_test.taint_number() == 1
    component_under_test.edit(
        0,
        datum('2.2.2012'),
        'zzName',
        'zzKategorie',
        2.34,
        'sebastian')
    assert component_under_test.taint_number() == 2
    assert component_under_test.get(0) == {
        'index': 0,
        'Datum': datum('2.2.2012'),
        'Kategorie': 'zzKategorie',
        'Name': 'zzName',
        'Wert': 2.34,
        'Person': 'sebastian'}


def test_delete_should_taint():
    component_under_test = Gemeinsamebuchungen()
    component_under_test.add(
        datum('1.1.2010'),
        'some kategorie',
        'some name',
        1.23,
        'sebastian')
    assert component_under_test.taint_number() == 1
    component_under_test.delete(0)
    assert component_under_test.taint_number() == 2


def test_rename_should_taint():
    component_under_test = Gemeinsamebuchungen()
    component_under_test.add(
        datum('1.1.2010'),
        'some kategorie',
        'some name',
        1.23,
        'sebastian')
    assert component_under_test.taint_number() == 1
    component_under_test.rename('sebastian', 'sebastian2')
    assert component_under_test.taint_number() == 2


def test_drop__with_matching_index__should_remove_data():
    component_under_test = Gemeinsamebuchungen()
    component_under_test.add(
        datum('1.1.2010'),
        'kategorie1',
        'name1',
        1.23,
        'person1')

    component_under_test.add(
        datum('2.2.2020'),
        'kategorie2',
        'name2',
        3.45,
        'person2')

    component_under_test.drop([1])

    assert component_under_test.select().to_list() == [
        {
            'index': 0,
            'Datum': datum('01.01.2010'),
            'Kategorie': 'kategorie1',
            'Name': 'name1',
            'Person': 'person1',
            'Wert': 1.23
        }
    ]


def test_drop_with__no_matching_index__should_remove_nothing():
    component_under_test = Gemeinsamebuchungen()
    component_under_test.add(
        datum('1.1.2010'),
        'kategorie1',
        'name1',
        1.23,
        'person1')

    component_under_test.add(
        datum('2.2.2020'),
        'kategorie2',
        'name2',
        3.45,
        'person2')

    component_under_test.drop([])

    assert component_under_test.select().to_list() == [
        {
            'index': 0,
            'Datum': datum('01.01.2010'),
            'Kategorie': 'kategorie1',
            'Name': 'name1',
            'Person': 'person1',
            'Wert': 1.23
        },
        {
            'index': 1,
            'Datum': datum('02.02.2020'),
            'Kategorie': 'kategorie2',
            'Name': 'name2',
            'Person': 'person2',
            'Wert': 3.45
        }
    ]


def test__get_content__with_no_entry__should_return_empty_list():
    component_under_test = Gemeinsamebuchungen()

    assert component_under_test.select().to_list() == []


def test__get_content__with_entries__should_return_list_of_dicts():
    component_under_test = Gemeinsamebuchungen()
    component_under_test.add(
        datum('1.1.2010'),
        'kategorie1',
        'name1',
        1.23,
        'person1')

    component_under_test.add(
        datum('2.2.2020'),
        'kategorie2',
        'name2',
        3.45,
        'person2')

    assert component_under_test.select().to_list() == [
        {
            'index': 0,
            'Datum': datum('01.01.2010'),
            'Kategorie': 'kategorie1',
            'Name': 'name1',
            'Person': 'person1',
            'Wert': 1.23
        },
        {
            'index': 1,
            'Datum': datum('02.02.2020'),
            'Kategorie': 'kategorie2',
            'Name': 'name2',
            'Person': 'person2',
            'Wert': 3.45
        }
    ]


def test_get_renamed_list():
    component_under_test = Gemeinsamebuchungen()

    component_under_test.add(
        datum('1.1.2020'),
        'kategorie1',
        'name1',
        1.11,
        'offline user')
    component_under_test.add(
        datum('2.2.2020'),
        'kategorie2',
        'name2',
        2.22,
        'offline partner')
    component_under_test.add(
        datum('3.3.2020'),
        'kategorie3',
        'name3',
        3.33,
        'unknown')

    result = component_under_test.get_renamed_list('offline user', 'online user', 'offline partner', 'online partner')

    assert result == [
        {
            'Datum': datum('1.1.2020'),
            'Name': 'name1',
            'Kategorie': 'kategorie1',
            'Wert': 1.11,
            'Person': 'online user'
        },
        {
            'Datum': datum('2.2.2020'),
            'Name': 'name2',
            'Kategorie': 'kategorie2',
            'Wert': 2.22,
            'Person': 'online partner'
        },
        {
            'Datum': datum('3.3.2020'),
            'Name': 'name3',
            'Kategorie': 'kategorie3',
            'Wert': 3.33,
            'Person': 'unknown'
        }
    ]


def test_drop_all():
    component_under_test = Gemeinsamebuchungen()

    component_under_test.add(
        datum('1.1.2020'),
        'kategorie1',
        'name1',
        1.11,
        'offline user')

    component_under_test.add(
        datum('1.1.2020'),
        'kategorie1',
        'name1',
        1.11,
        'offline user')

    component_under_test.drop_all()

    assert len(component_under_test.content) == 0
    assert component_under_test.tainted
