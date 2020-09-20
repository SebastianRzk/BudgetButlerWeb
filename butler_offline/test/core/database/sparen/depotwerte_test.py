import unittest
from butler_offline.core.database.sparen.depotwerte import Depotwerte


class DepotweteTest(unittest.TestCase):

    def test_add_shouldAdd(self):
        component_under_test = Depotwerte()

        component_under_test.add(name='1name', isin='some isin')

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Name[0] == '1name'
        assert component_under_test.content.ISIN[0] == 'some isin'

    def test_edit_shouldEdit(self):
        component_under_test = Depotwerte()

        component_under_test.add('0name', '0isin',)
        component_under_test.add('1name', '1isin',)
        component_under_test.add('2name', '2isin',)

        assert len(component_under_test.content) == 3
        element_before = component_under_test.get(1)
        assert element_before == {
            'index': 1,
            'Name': '1name',
            'ISIN': '1isin'
        }

        component_under_test.edit(index=1, name='13name', isin='13isin')

        assert len(component_under_test.content) == 3
        element_after = component_under_test.get(1)
        assert element_after == {
            'index': 1,
            'Name': '13name',
            'ISIN': '13isin'
        }

    def test_get_depotwerte(self):
        component_under_test = Depotwerte()

        component_under_test.add('0name', '0isin',)
        component_under_test.add('1name', '1isin',)

        assert component_under_test.get_depotwerte() == ['0isin', '1isin']

if __name__ == '__main__':
    unittest.main()
