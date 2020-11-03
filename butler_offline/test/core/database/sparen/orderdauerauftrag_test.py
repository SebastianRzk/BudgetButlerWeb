import unittest
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.core.database.sparen.order import Order


def test_add_should_add():
    component_under_test = OrderDauerauftrag()

    component_under_test.add(datum('01.01.2020'), datum('01.01.2021'), 'monatlich', '1name', '1konto', '1depotwert', 100)

    assert len(component_under_test.content) == 1
    assert component_under_test.content.Startdatum[0] == datum('01.01.2020')
    assert component_under_test.content.Endedatum[0] == datum('01.01.2021')
    assert component_under_test.content.Rhythmus[0] == 'monatlich'
    assert component_under_test.content.Name[0] == '1name'
    assert component_under_test.content.Konto[0] == '1konto'
    assert component_under_test.content.Depotwert[0] == '1depotwert'
    assert component_under_test.content.Wert[0] == 100


def test_edit_should_edit():
    component_under_test = OrderDauerauftrag()

    component_under_test.add(datum('01.01.2020'), datum('01.01.2021'), 'monatlich', '1name', '1konto', '1depotwert', 100)
    component_under_test.add(datum('02.02.2020'), datum('02.02.2021'), 'monatlich', '2name', '2konto', '2depotwert', 200)
    component_under_test.add(datum('03.03.2020'), datum('03.03.2021'), 'monatlich', '3name', '3konto', '3depotwert', 300)

    assert len(component_under_test.content) == 3
    element_before = component_under_test.get(1)
    assert element_before == {
        'index': 1,
        'Startdatum': datum('02.02.2020'),
        'Endedatum': datum('02.02.2021'),
        'Rhythmus': 'monatlich',
        'Name': '2name',
        'Konto': '2konto',
        'Depotwert': '2depotwert',
        'Wert': 200
    }

    component_under_test.edit(1, datum('03.02.2020'), datum('03.02.2021'), 'jährlich', '24name', '24konto', '24depotwert', 240)

    assert len(component_under_test.content) == 3
    element_after = component_under_test.get(1)
    assert element_after == {
        'index': 1,
        'Startdatum': datum('03.02.2020'),
        'Endedatum': datum('03.02.2021'),
        'Rhythmus': 'jährlich',
        'Name': '24name',
        'Konto': '24konto',
        'Depotwert': '24depotwert',
        'Wert': 240
    }


def test_order_until_today_with_invalid_dates_should_be_empty():
    component_under_test = OrderDauerauftrag()

    component_under_test.add(datum('01.01.2020'), datum('01.01.2019'), 'monatlich', 'invalid', '1konto', '1depotwert', 222)

    result = component_under_test.get_all_order_until_today()

    assert len(result) == 0


def test_order_until_today_with_date_in_future_should_be_empty():
    component_under_test = OrderDauerauftrag()

    component_under_test.add(datum('01.01.3020'), datum('01.01.3021'), 'monatlich', 'future', '1konto', '1depotwert', 333)

    result = component_under_test.get_all_order_until_today()

    assert len(result) == 0


def test_order_until_today():
    component_under_test = OrderDauerauftrag()

    component_under_test.add(datum('01.01.2020'), datum('02.02.2020'), 'monatlich', '1name', '1konto', '1depotwert', 100)

    result = component_under_test.get_all_order_until_today()

    assert len(result) == 2
    assert result.Datum[0] == datum('01.01.2020')
    assert result.Name[0] == '1name'
    assert result.Konto[0] == '1konto'
    assert result.Depotwert[0] == '1depotwert'
    assert result.Wert[0] == 100

    assert result.Datum[1] == datum('01.02.2020')
    assert result.Name[1] == '1name'
    assert result.Konto[1] == '1konto'
    assert result.Depotwert[1] == '1depotwert'
    assert result.Wert[1] == 100


def test_order_until_today_table_header_should_comply_order_table_header():
    component_under_test = OrderDauerauftrag()

    component_under_test.add(datum('01.01.2020'), datum('02.02.2020'), 'monatlich', '1name', '1konto', '1depotwert', 100)

    result = component_under_test.get_all_order_until_today()

    assert sorted(result.columns) == sorted(Order.TABLE_HEADER)


def test_get_past_should_only_return_past():
    component_under_test = OrderDauerauftrag()

    component_under_test.add(
        datum('01.01.2020'), datum('02.02.2020'), 'monatlich', '1name', '1konto', '1depotwert', 100)
    component_under_test.add(
        datum('01.01.2020'), datum('02.02.2050'), 'monatlich', 'future', '1konto', '1depotwert', 100)

    result = component_under_test.past()

    assert len(result) == 1
    assert result[0]['Name'] == '1name'


def test_get_aktuelle_should_only_return_current():
    component_under_test = OrderDauerauftrag()

    component_under_test.add(
        datum('01.01.2020'), datum('02.02.2020'), 'monatlich', 'past', '1konto', '1depotwert', 100)
    component_under_test.add(
        datum('01.01.2020'), datum('02.02.2050'), 'monatlich', '1name', '1konto', '1depotwert', 100)
    component_under_test.add(
        datum('01.01.2050'), datum('02.02.2050'), 'monatlich', 'future', '1konto', '1depotwert', 100)

    result = component_under_test.aktuelle()

    assert len(result) == 1
    assert result[0]['Name'] == '1name'


def test_get_future_should_only_return_future():
    component_under_test = OrderDauerauftrag()

    component_under_test.add(
        datum('01.01.2020'), datum('02.02.2050'), 'monatlich', 'current', '1konto', '1depotwert', 100)
    component_under_test.add(
        datum('01.01.2050'), datum('02.02.2050'), 'monatlich', '1name', '1konto', '1depotwert', 100)

    result = component_under_test.future()

    assert len(result) == 1
    assert result[0]['Name'] == '1name'


if __name__ == '__main__':
    unittest.main()
