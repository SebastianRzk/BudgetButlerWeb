import unittest
from butler_offline.core.database.sparen.depotwerte import Depotwerte


def test_add_shouldAdd():
    component_under_test = Depotwerte()

    component_under_test.add(name='1name', isin='some isin', typ= component_under_test.TYP_ETF)

    assert len(component_under_test.content) == 1
    assert component_under_test.content.Name[0] == '1name'
    assert component_under_test.content.ISIN[0] == 'some isin'
    assert component_under_test.content.Typ[0] == component_under_test.TYP_ETF


def test_edit_shouldEdit():
    component_under_test = Depotwerte()

    component_under_test.add('0name', '0isin', typ=component_under_test.TYP_ETF)
    component_under_test.add('1name', '1isin', typ=component_under_test.TYP_ETF)
    component_under_test.add('2name', '2isin', typ=component_under_test.TYP_ETF)

    assert len(component_under_test.content) == 3
    element_before = component_under_test.get(1)
    assert element_before == {
        'index': 1,
        'Name': '1name',
        'Typ': component_under_test.TYP_ETF,
        'ISIN': '1isin'
    }

    component_under_test.edit(index=1, name='13name', isin='13isin', typ=component_under_test.TYP_FOND)

    assert len(component_under_test.content) == 3
    element_after = component_under_test.get(1)
    assert element_after == {
        'index': 1,
        'Name': '13name',
        'Typ': component_under_test.TYP_FOND,
        'ISIN': '13isin'
    }


def test_get_depotwerte():
    component_under_test = Depotwerte()

    component_under_test.add(name='0name', isin='0isin', typ=component_under_test.TYP_ETF)
    component_under_test.add(name='1name', isin='1isin', typ=component_under_test.TYP_ETF)

    assert component_under_test.get_depotwerte() == ['0isin', '1isin']


def test_get_valid_isins():
    component_under_test = Depotwerte()

    component_under_test.add(name='invalid isin', isin='-', typ=component_under_test.TYP_ETF)
    component_under_test.add(name='valid isin', isin='isin56789012', typ=component_under_test.TYP_ETF)

    assert component_under_test.get_valid_isins() == ['isin56789012']


if __name__ == '__main__':
    unittest.main()
