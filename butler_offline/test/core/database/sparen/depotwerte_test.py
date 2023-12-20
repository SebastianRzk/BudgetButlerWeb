from butler_offline.core.database.sparen.depotwerte import Depotwerte
import pandas as pd
from butler_offline.test.core.database import extract_index, extract_name_column


def test_add_should_add():
    component_under_test = Depotwerte()

    component_under_test.add(name='1name', isin='some isin', typ=component_under_test.TYP_ETF)

    assert len(component_under_test.content) == 1
    assert component_under_test.content.Name[0] == '1name'
    assert component_under_test.content.ISIN[0] == 'some isin'
    assert component_under_test.content.Typ[0] == component_under_test.TYP_ETF


def test_edit_should_edit():
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


def test_add_should_sort_and_drop_index():
    component_under_test = Depotwerte()

    component_under_test.add('name2', '1isin', typ=component_under_test.TYP_ETF)
    component_under_test.add('name1', '1isin', typ=component_under_test.TYP_ETF)

    assert extract_name_column(component_under_test) == ['name1', 'name2']
    assert extract_index(component_under_test) == [0, 1]


def test_edit_should_sort_and_drop_index():
    component_under_test = Depotwerte()

    component_under_test.add('name1', '1isin', typ=component_under_test.TYP_ETF)
    component_under_test.add('name2', '1isin', typ=component_under_test.TYP_ETF)

    component_under_test.edit(1, 'name0', '1isin', typ=component_under_test.TYP_ETF)

    assert extract_name_column(component_under_test) == ['name0', 'name1']
    assert extract_index(component_under_test) == [0, 1]


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


def check_equal(left, right):
    return len(left) == len(right) and sorted(left) == sorted(right)


def test_parse_and_migrate_without_type_shoud_set_type_etf():
    depotwerte = Depotwerte()
    raw_table = pd.DataFrame([["demoname", "demoisin"]], columns=['Name', 'ISIN'])

    depotwerte.parse_and_migrate(raw_table)

    assert check_equal(depotwerte.content.columns, Depotwerte.TABLE_HEADER)
    assert len(depotwerte.content) == 1
    assert depotwerte.content.Name[0] == 'demoname'
    assert depotwerte.content.ISIN[0] == 'demoisin'
    assert depotwerte.content.Typ[0] == Depotwerte.TYP_ETF


def test_get_isin_nach_typ_with_empty_db_should_return_empty():
    depotwerte = Depotwerte()

    assert not depotwerte.get_isin_nach_typ()


def test_get_isin_nach_typ():
    depotwerte = Depotwerte()
    depotwerte.add('Name_Etf1', 'ISIN_Etf1', depotwerte.TYP_ETF)
    depotwerte.add('Name_Etf2', 'ISIN_Etf2', depotwerte.TYP_ETF)
    depotwerte.add('Name_Fond', 'ISIN_Fond', depotwerte.TYP_FOND)

    result = depotwerte.get_isin_nach_typ()

    assert len(result.keys()) == 2
    assert result[depotwerte.TYP_ETF] == ['ISIN_Etf1', 'ISIN_Etf2']
    assert result[depotwerte.TYP_FOND] == ['ISIN_Fond']
