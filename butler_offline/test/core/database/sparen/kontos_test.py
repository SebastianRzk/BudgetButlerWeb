import unittest
from butler_offline.core.database.sparen.kontos import Kontos


class KontosTest(unittest.TestCase):

    def test_add_shouldAdd(self):
        component_under_test = Kontos()

        component_under_test.add(kontoname='1name', kontotyp='1typ')

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Kontoname[0] == '1name'
        assert component_under_test.content.Kontotyp[0] == '1typ'

    def test_edit_shouldEdit(self):
        component_under_test = Kontos()

        component_under_test.add('0name', '0typ',)
        component_under_test.add('1name', '1typ',)
        component_under_test.add('2name', '2typ',)

        assert len(component_under_test.content) == 3
        element_before = component_under_test.get(1)
        assert element_before == {
            'index': 1,
            'Kontoname': '1name',
            'Kontotyp': '1typ'
        }

        component_under_test.edit(index=1, kontoname='13name', kontotyp='13typ')

        assert len(component_under_test.content) == 3
        element_after = component_under_test.get(1)
        assert element_after == {
            'index': 1,
            'Kontoname': '13name',
            'Kontotyp': '13typ'
        }

    def test_get_sparfaehige_kontos(self):
        component_under_test = Kontos()
        component_under_test.add(kontoname='Spar', kontotyp=Kontos.TYP_SPARKONTO)
        component_under_test.add(kontoname='Geno', kontotyp=Kontos.TYP_GENOSSENSCHAFTSANTEILE)
        component_under_test.add(kontoname='Depot', kontotyp=Kontos.TYP_DEPOT)
        component_under_test.add(kontoname='Sonst', kontotyp='Sonstiges')

        result = component_under_test.get_sparfaehige_kontos()

        assert set(result) == {'Geno', 'Spar'}

    def test_get_depot(self):
        component_under_test = Kontos()
        component_under_test.add(kontoname='Spar', kontotyp=Kontos.TYP_SPARKONTO)
        component_under_test.add(kontoname='Geno', kontotyp=Kontos.TYP_GENOSSENSCHAFTSANTEILE)
        component_under_test.add(kontoname='Depot', kontotyp=Kontos.TYP_DEPOT)
        component_under_test.add(kontoname='Sonst', kontotyp='Sonstiges')

        result = component_under_test.get_depots()

        assert set(result) == {'Depot'}


if __name__ == '__main__':
    unittest.main()
