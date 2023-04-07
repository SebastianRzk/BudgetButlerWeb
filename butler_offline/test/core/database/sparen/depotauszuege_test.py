from datetime import timedelta
from butler_offline.core import time
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.test.core.database import extract_index, extract_column_values


def test_add_should_add():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('01.01.2020'), 'demoisin', 'demokonto', 100)

    assert len(component_under_test.content) == 1
    assert component_under_test.content.Datum[0] == datum('01.01.2020')
    assert component_under_test.content.Depotwert[0] == 'demoisin'
    assert component_under_test.content.Konto[0] == 'demokonto'
    assert component_under_test.content.Wert[0] == 100


def test_edit_should_edit():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('01.01.2020'), '1demoisin', '1demokonto', 100)
    component_under_test.add(datum('02.02.2020'), '2demoisin', '2demokonto', 200)
    component_under_test.add(datum('03.03.2020'), '3demoisin', '3demokonto', 300)

    assert len(component_under_test.content) == 3
    element_before = component_under_test.get(1)
    assert element_before == {
        'index': 1,
        'Datum': datum('02.02.2020'),
        'Depotwert': '2demoisin',
        'Konto': '2demokonto',
        'Wert': 200
    }

    component_under_test.edit(1, datum('03.02.2020'), '23demoisin', '23demokonto', 230)

    assert len(component_under_test.content) == 3
    element_after = component_under_test.get(1)
    assert element_after == {
        'index': 1,
        'Datum': datum('03.02.2020'),
        'Depotwert': '23demoisin',
        'Konto': '23demokonto',
        'Wert': 230
    }


def test_add_should_sort_and_drop_index():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('01.01.2020'), 'depotwert1', '1demokonto', 100)
    component_under_test.add(datum('01.01.2010'), 'depotwert2', '1demokonto', 100)

    assert extract_column_values(component_under_test, 'Depotwert') == ['depotwert2', 'depotwert1']
    assert extract_index(component_under_test) == [0, 1]


def test_edit_should_sort_and_drop_index():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('01.01.2010'), 'depotwert1', '1demokonto', 100)
    component_under_test.add(datum('01.01.2020'), 'depotwert2', '1demokonto', 100)

    component_under_test.edit(1, datum('01.01.2000'), 'depotwert2', '1demokonto', 100)

    assert extract_column_values(component_under_test, 'Depotwert') == ['depotwert2', 'depotwert1']
    assert extract_index(component_under_test) == [0, 1]


def test_get_by():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('01.01.2020'), 'demoisin', '1demokonto', 100)
    component_under_test.add(datum('02.01.2020'), 'demoisin', '1demokonto', 200)
    component_under_test.add(datum('01.01.2020'), 'demoisin', '2demokonto', 300)

    result = component_under_test.get_by(datum('01.01.2020'), '1demokonto')

    assert len(result) == 1
    assert result.index[0] == 0
    assert result.Datum[0] == datum('01.01.2020')
    assert result.Depotwert[0] == 'demoisin'
    assert result.Konto[0] == '1demokonto'
    assert result.Wert[0] == 100


def test_resolve_index():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('01.01.2020'), 'demoisin', '1demokonto', 100)
    component_under_test.add(datum('02.01.2020'), 'demoisin', '1demokonto', 200)
    component_under_test.add(datum('02.01.2020'), 'demoisin2', '1demokonto', 200)
    component_under_test.add(datum('01.01.2020'), 'demoisin', '2demokonto', 300)

    assert component_under_test.resolve_index(datum('01.01.2020'), '1demokonto', 'demoisin') == 0
    assert component_under_test.resolve_index(datum('02.01.2020'), '1demokonto', 'demoisin') == 2
    assert component_under_test.resolve_index(datum('02.01.2020'), '1demokonto', 'demoisin2') == 3
    assert component_under_test.resolve_index(datum('01.01.2020'), '2demokonto', 'demoisin') == 1


def test_get_latest_datum_by():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('01.01.2020'), 'demoisin', '1demokonto', 100)
    component_under_test.add(datum('02.01.2020'), 'demoisin', '1demokonto', 200)
    component_under_test.add(datum('03.01.2020'), 'demoisin', '2demokonto', 300)

    assert component_under_test.get_latest_datum_by('1demokonto') == datum('02.01.2020')


def test_get_latest_datum_by_with_not_content_should_return_none():
    component_under_test = Depotauszuege()

    assert not component_under_test.get_latest_datum_by('1demokonto')


def test_exists_wert():
    component_under_test = Depotauszuege()

    assert not component_under_test.exists_wert(depotwert='isin1', konto='konto1')

    component_under_test.add(datum('01.01.2020'), 'isin1', 'konto1', 100)

    assert component_under_test.exists_wert(depotwert='isin1', konto='konto1')


def test_get_kontostand_by_with_empty_should_return_zero():
    component_under_test = Depotauszuege()

    assert component_under_test.get_kontostand_by('demokonto') == 0


def test_get_kontostand_by_():
    component_under_test = Depotauszuege()
    component_under_test.add(datum('01.01.2020'), '1isin', 'demokonto', 10)

    component_under_test.add(datum('02.01.2020'), '1isin', 'demokonto', 200)
    component_under_test.add(datum('02.01.2020'), '2isin', 'demokonto', 300)
    component_under_test.add(datum('02.01.2020'), '1isin', '1demokonto', 999)

    assert component_under_test.get_kontostand_by('demokonto') == 500


def test_get_depotwert_by_with_empty_should_return_zero():
    component_under_test = Depotauszuege()

    assert component_under_test.get_depotwert_by('isin1') == 0


def test_get_depotwert_by():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('01.01.2020'), '1isin', '1demokonto', 11)

    component_under_test.add(datum('02.01.2020'), '1isin', '1demokonto', 200)
    component_under_test.add(datum('02.01.2020'), '2isin', '1demokonto', 311)
    component_under_test.add(datum('02.01.2020'), '1isin', '2demokonto', 400)

    assert component_under_test.get_depotwert_by('1isin') == 600


def test_resolve_konto():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('03.01.2020'), '1isin', '1demokonto', 11)
    component_under_test.add(datum('07.01.2020'), '1isin', '2demokonto', 11)
    component_under_test.add(datum('01.01.2020'), '1isin', '3demokonto', 11)

    assert component_under_test.resolve_konto(1) == '1demokonto'


def test_resolve_datum():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('03.01.2020'), '1isin', '1demokonto', 11)
    component_under_test.add(datum('07.01.2020'), '1isin', '2demokonto', 11)
    component_under_test.add(datum('01.01.2020'), '1isin', '3demokonto', 11)

    assert component_under_test.resolve_datum(1) == datum('03.01.2020')


def test_select_max_year():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('03.01.2019'), '1isin', '1demokonto', 11)
    component_under_test.add(datum('05.01.2020'), '1isin', '1demokonto', 12)
    component_under_test.add(datum('03.01.2021'), '1isin', '1demokonto', 99)
    component_under_test.add(datum('03.01.2022'), '1isin', '1demokonto', 99)

    assert component_under_test.select_max_year(2020).get_kontostand_by('1demokonto') == 12


def test_delete_depotauszug():
    component_under_test = Depotauszuege()

    component_under_test.add(datum('01.01.2020'), '1isin', '1demokonto', 1)
    component_under_test.add(datum('03.01.2020'), '2isin', '2demokonto', 2)
    component_under_test.add(datum('03.01.2020'), '3isin', '2demokonto', 3)
    component_under_test.add(datum('03.01.2020'), '4isin', '3demokonto', 4)

    assert len(component_under_test.content) == 4

    component_under_test.delete_depotauszug(datum('03.01.2020'), '2demokonto')

    assert len(component_under_test.content) == 2
    assert component_under_test.content.index.tolist() == [0, 3]
    assert component_under_test.content.Datum.tolist() == [datum('01.01.2020'), datum('03.01.2020')]
    assert component_under_test.content.Depotwert.tolist() == ['1isin', '4isin']
    assert component_under_test.content.Wert.tolist() == [1, 4]


def test_get_isins_invested_by_should_use_today_if_no_value_present():
    component_under_test = Depotauszuege()

    component_under_test.add(time.today(), '1isin1234567', '1demokonto', 1)
    component_under_test.add(time.today() + timedelta(days=1), '2isin1234567', '2demokonto', 2)

    assert component_under_test.get_isins_invested_by() == ['1isin1234567']


def test_get_isins_invested_by_should_filter_out_not_invested_etfs_to_that_time():
    component_under_test = Depotauszuege()

    component_under_test.add(time.today(), '1isin1234567', '1demokonto', 1)
    component_under_test.add(time.today() - timedelta(days=1), '2isin1234567', '2demokonto', 2)
    component_under_test.add(time.today(), '2isin1234567', '2demokonto', 0)

    assert component_under_test.get_isins_invested_by() == ['1isin1234567']


def test_get_isins_invested_by_should_order_by_invested_value():
    component_under_test = Depotauszuege()

    component_under_test.add(time.today(), 'mid_12345678', '2demokonto', 222)
    component_under_test.add(time.today(), 'small_123456', '1demokonto', 111)
    component_under_test.add(time.today(), 'large_123456', '2demokonto', 333)

    assert component_under_test.get_isins_invested_by() == ['large_123456', 'mid_12345678', 'small_123456']


def test_get_isins_invested_by_should_filter_invalid_isins():
    component_under_test = Depotauszuege()

    component_under_test.add(time.today(), 'too_long_12342342345', '2demokonto', 222)
    component_under_test.add(time.today(), 'isin_1234567', '1demokonto', 111)
    component_under_test.add(time.today(), 'too_short', '2demokonto', 333)

    assert component_under_test.get_isins_invested_by() == ['isin_1234567']
