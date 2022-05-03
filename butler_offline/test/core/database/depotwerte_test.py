from butler_offline.core.database.sparen.depotwerte import Depotwerte
import pandas as pd

def check_equal(L1, L2):
    return len(L1) == len(L2) and sorted(L1) == sorted(L2)


def test_parse_and_migrate_with_existing_data_should_do_nothing():
    depotwerte = Depotwerte()
    raw_table = pd.DataFrame([["demoname", "demoisin", Depotwerte.TYP_FOND]], columns=Depotwerte.TABLE_HEADER)

    depotwerte.parse_and_migrate(raw_table)

    assert check_equal(depotwerte.content.columns, Depotwerte.TABLE_HEADER)
    assert len(depotwerte.content) == 1
    assert depotwerte.content.Name[0] == 'demoname'
    assert depotwerte.content.ISIN[0] == 'demoisin'
    assert depotwerte.content.Typ[0] == Depotwerte.TYP_FOND


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
