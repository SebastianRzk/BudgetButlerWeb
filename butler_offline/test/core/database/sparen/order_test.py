import unittest
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.sparen.order import Order
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen


class OrderTest(unittest.TestCase):

    def test_add_shouldAdd(self):
        component_under_test = Order()

        component_under_test.add(datum('01.01.2020'), '1name', '1konto', '1depotwert', 100)

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Datum[0] == datum('01.01.2020')
        assert component_under_test.content.Name[0] == '1name'
        assert component_under_test.content.Konto[0] == '1konto'
        assert component_under_test.content.Depotwert[0] == '1depotwert'
        assert component_under_test.content.Wert[0] == 100

    def test_edit_shouldEdit(self):
        component_under_test = Order()

        component_under_test.add(datum('01.01.2020'), '1name', '1konto', '1depotwert', 100)
        component_under_test.add(datum('02.02.2020'), '2name', '2konto', '2depotwert', 200)
        component_under_test.add(datum('03.03.2020'), '3name', '3konto', '3depotwert', 300)

        assert len(component_under_test.content) == 3
        element_before = component_under_test.get(1)
        assert element_before == {
            'index': 1,
            'Datum': datum('02.02.2020'),
            'Name': '2name',
            'Konto': '2konto',
            'Depotwert': '2depotwert',
            'Wert': 200
        }

        component_under_test.edit(1, datum('03.02.2020'), '24name', '24konto', '24depotwert', 240)

        assert len(component_under_test.content) == 3
        element_after = component_under_test.get(1)
        assert element_after == {
            'index': 1,
            'Datum': datum('03.02.2020'),
            'Name': '24name',
            'Konto': '24konto',
            'Depotwert': '24depotwert',
            'Wert': 240
        }

    def test_get_dynamische_einzelbuchungen(self):
        component_under_test = Order()

        component_under_test.add(datum('01.01.2020'), '1name', '1konto', '1depotwert', 100)

        result = component_under_test.get_dynamische_einzelbuchungen()

        assert len(result) == 1
        assert set(result.columns) == set(Einzelbuchungen.TABLE_HEADER)

        assert result.Datum[0] == datum('01.01.2020')
        assert result.Name[0] == '1name'
        assert result.Kategorie[0] == 'Sparen'
        assert result.Wert[0] == -100
        assert result.Dynamisch[0]
        assert not result.Tags[0]

    def test_get_order_fuer(self):
        component_under_test = Order()

        component_under_test.add(datum('01.01.2020'), '1name', '1konto', '1depotwert', 100)
        component_under_test.add(datum('01.01.2020'), '1name', '2konto', '1depotwert', 300)

        assert component_under_test.get_order_fuer('1konto') == 100

    def test_get_order_fuer_depotwert(self):
        component_under_test = Order()

        component_under_test.add(datum('01.01.2020'), '1name', '1konto', '1depotwert', 100)
        component_under_test.add(datum('01.01.2020'), '1name', '2konto', '2depotwert', 300)

        assert component_under_test.get_order_fuer_depotwert('1depotwert') == 100

    def test_select_year(self):
        component_under_test = Order()

        component_under_test.add(datum('01.01.2020'), '1name', '1konto', '1depotwert', 100)
        component_under_test.add(datum('01.01.2021'), '1name', '1konto', '2depotwert', 300)
        component_under_test.add(datum('01.01.2022'), '1name', '1konto', '2depotwert', 500)

        assert component_under_test.select_year(2021).get_order_fuer('1konto') == 300



if __name__ == '__main__':
    unittest.main()
