from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen


def test__select_range__with_entries_containing_matching_dates__should_return_entries():
    component_under_test = Gemeinsamebuchungen()
    component_under_test.add(
        datum('01.01.2010'),
        'some kategorie',
        'some name',
        1.23,
        'sebastian')

    assert component_under_test.select().select_range(datum('01.01.2009'), datum('01.01.2011')).to_list() == [{
        'Datum': datum('01.01.2010'),
        'Kategorie': 'some kategorie',
        'Name': 'some name',
        'Wert': 1.23,
        'Person': 'sebastian',
        'index': 0
    }]


def test__select_range__with_out_of_range_entries__should_filter_them_out():
    component_under_test = Gemeinsamebuchungen()
    component_under_test.add(
        datum('01.01.2010'),
        'some kategorie',
        'some name',
        1.23,
        'sebastian')
    component_under_test.add(
        datum('01.01.2000'),
        'xxxx',
        'xxxx',
        0.00,
        'xxxx')
    component_under_test.add(
        datum('01.01.2020'),
        'yyyy',
        'yyyy',
        0.00,
        'yyyy')

    assert component_under_test.select().select_range(datum('01.01.2009'), datum('01.01.2011')).to_list() == [{
        'Datum': datum('01.01.2010'),
        'Kategorie': 'some kategorie',
        'Name': 'some name',
        'Wert': 1.23,
        'Person': 'sebastian',
        'index': 1
    }]
