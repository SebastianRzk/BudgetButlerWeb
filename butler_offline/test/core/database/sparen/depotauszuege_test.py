import unittest
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.viewcore.converter import datum_from_german as datum

class DepotauszuegeTest(unittest.TestCase):

    def test_add_shouldAdd(self):
        component_under_test = Depotauszuege()

        component_under_test.add(datum('01.01.2020'), 'demoisin', 'demokonto', 100)

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Datum[0] == datum('01.01.2020')
        assert component_under_test.content.Depotwert[0] == 'demoisin'
        assert component_under_test.content.Konto[0] == 'demokonto'
        assert component_under_test.content.Wert[0] == 100

    def test_edit_shouldEdit(self):
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


    def test_get_by(self):
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

    def test_resolve_index(self):
        component_under_test = Depotauszuege()

        component_under_test.add(datum('01.01.2020'), 'demoisin', '1demokonto', 100)
        component_under_test.add(datum('02.01.2020'), 'demoisin', '1demokonto', 200)
        component_under_test.add(datum('02.01.2020'), 'demoisin2', '1demokonto', 200)
        component_under_test.add(datum('01.01.2020'), 'demoisin', '2demokonto', 300)

        component_under_test.resolve_index(datum('01.01.2020'), '1demokonto', 'demoisin') == 0
        component_under_test.resolve_index(datum('02.01.2020'), '1demokonto', 'demoisin') == 1
        component_under_test.resolve_index(datum('02.01.2020'), '1demokonto', 'demoisin2') == 2
        component_under_test.resolve_index(datum('01.01.2020'), '2demokonto', 'demoisin') == 3

    def test_get_latest_datum_by(self):
        component_under_test = Depotauszuege()

        component_under_test.add(datum('01.01.2020'), 'demoisin', '1demokonto', 100)
        component_under_test.add(datum('02.01.2020'), 'demoisin', '1demokonto', 200)
        component_under_test.add(datum('03.01.2020'), 'demoisin', '2demokonto', 300)

        assert component_under_test.get_latest_datum_by('1demokonto') == datum('02.01.2020')

    def test_get_latest_datum_by_with_not_content_should_return_none(self):
        component_under_test = Depotauszuege()

        assert not component_under_test.get_latest_datum_by('1demokonto')

    def test_exists_wert(self):
        component_under_test = Depotauszuege()

        assert not component_under_test.exists_wert(depotwert='isin1', konto='konto1')

        component_under_test.add(datum('01.01.2020'), 'isin1', 'konto1', 100)

        assert component_under_test.exists_wert(depotwert='isin1', konto='konto1')


if __name__ == '__main__':
    unittest.main()
