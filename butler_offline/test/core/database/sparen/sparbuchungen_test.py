import unittest
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen


class SparbuchungenTest(unittest.TestCase):

    def test_get_static_content_should_filter_dynamic_content(self):
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

    def test_add_shouldAdd(self):
        component_under_test = Sparbuchungen()

        component_under_test.add(datum('01.01.2012'), '1name', 1, '1typ', '1konto', dynamisch=True)

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Datum[0] == datum('01.01.2012')
        assert component_under_test.content.Typ[0] == '1typ'
        assert component_under_test.content.Name[0] == '1name'
        assert component_under_test.content.Wert[0] == 1
        assert component_under_test.content.Konto[0] == '1konto'
        assert component_under_test.content.Dynamisch[0]

    def test_edit_shouldEdit(self):
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

if __name__ == '__main__':
    unittest.main()
