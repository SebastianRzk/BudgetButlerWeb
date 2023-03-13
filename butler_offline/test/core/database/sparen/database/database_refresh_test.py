from butler_offline.core.database import Database
from butler_offline.viewcore.converter import datum_from_german as datum


def teste_refresh_with_empty_database():
    component_under_test = Database('test_database')
    component_under_test.refresh()


def teste_refresh_should_add_einzelbuchungen_von_dauerauftrag():
    component_under_test = Database('test_database')
    component_under_test.dauerauftraege.add(datum('10.01.2010'), datum('11.03.2010'), '', '', 'monatlich', 20)
    component_under_test.refresh()

    assert component_under_test.einzelbuchungen.select().count() == 3


def test_refresh_should_add_order_and_einzelbuchung_on_orderdauerauftrag():
    component_under_test = Database('test_database')
    component_under_test.orderdauerauftrag.add(
        datum('01.01.2020'),
        datum('02.01.2020'),
        'monatlich',
        '1name',
        '1konto',
        '1depotwert',
        100)

    component_under_test.refresh()

    assert component_under_test.order.select().count() == 1
    assert component_under_test.einzelbuchungen.select().count() == 1
