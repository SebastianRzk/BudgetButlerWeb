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




if __name__ == '__main__':
    unittest.main()
