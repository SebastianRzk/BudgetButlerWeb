from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.viewcore.converter import datum_from_german as datum


def test_inject_zeroes_for_year_and_kategories__should_inject_zeroes():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.02.2017'), 'kat1', '', 5,)
    component_under_test.add(datum('01.02.2017'), 'kat2', '', 5,)
    result = component_under_test.select().inject_zeroes_for_year_and_kategories(2017).raw_table()
    assert len(result) == 26
    assert datum('01.01.2017') in set(result.Datum)
    assert datum('01.12.2017') in set(result.Datum)
    assert result.Wert.sum() == 10
    assert {'kat1', 'kat2'} == set(result.Kategorie)


def test_sum_kategorien_monthly():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.02.2017'), 'kat1', '', 5,)
    component_under_test.add(datum('01.02.2017'), 'kat2', '', 10,)
    result = component_under_test.select().sum_kategorien_monthly()
    assert len(result) == 1
    assert len(result[2]) == 2
    assert result[2]['kat1'] == '5.00'
    assert result[2]['kat2'] == '10.00'


def test_inject_zeroes_for_year_and_kategories__with_no_values__should_inject_zeroes():
    component_under_test = Einzelbuchungen()
    assert component_under_test.select().inject_zeroes_for_year_and_kategories(2017).sum() == 0


def test__inject_zeros__should_inject_zeroes():
    component_under_test = Einzelbuchungen()
    select = component_under_test.select()

    assert len(select.content) == 0

    select = select.inject_zeros_for_year(2017)
    assert len(select.content) == 12
    assert select.content.loc[0].Datum == datum('01.01.2017')
    assert select.content.loc[11].Datum == datum('01.12.2017')
    assert select.content.Wert.sum() == 0


def test__sum_monthly__with_unique_months():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.01.2017'), '', '', 20,)
    component_under_test.add(datum('01.02.2017'), '', '', 10,)

    result = component_under_test.select().sum_monthly()

    assert result == ['20.00', '10.00']


def test__sum_monthly__with_duplicated_months__should_sum_values():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('01.02.2017'), '', '', 5,)
    component_under_test.add(datum('01.01.2017'), '', '', 20,)
    component_under_test.add(datum('01.02.2017'), '', '', 10,)

    result = component_under_test.select().sum_monthly()

    assert result == ['20.00', '15.00']


def test_sum__with_empty_db__should_return_zero():
    component_under_test = Einzelbuchungen()
    assert component_under_test.select().sum() == 0


def test_sum__with_buchung__should_return_value():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('1.1.2010'), '', '', 10)

    assert component_under_test.select().sum() == 10


def test__filter_year__with_non_matching_year__should_remove_item():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('1.1.2010'), '', '', 10)

    assert component_under_test.select().select_year(2011).sum() == 0


def test__filter_year__with_matching_year__should_return_value():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('1.1.2011'), '', '', 10)

    assert component_under_test.select().select_year(2011).sum() == 10


def test_einnahmen__with_einnahme__should_return_value():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('1.1.2011'), '', '', 10)

    assert component_under_test.select().select_einnahmen().select_year(2011).sum() == 10


def test_einnahmen_withAusgabe_shoudReturnZero():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('1.1.2011'), '', '', -10)

    assert component_under_test.select().select_einnahmen().select_year(2011).sum() == 0


def test_ausgaben_withEinnahme_shoudReturnZero():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('1.1.2011'), '', '', 10)

    assert component_under_test.select().select_ausgaben().select_year(2011).sum() == 0


def test_ausgaben_withAusgabe_shoudReturnValue():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('1.1.2011'), '', '', -10)

    assert component_under_test.select().select_ausgaben().select_year(2011).sum() == -10


def test_select_withMonthSelection_andMatchingMonth_shouldReturnValue():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('1.1.2011'), '', '', -10)

    assert component_under_test.select().select_month(1).sum() == -10


def test_select_withMonthSelection_andEmptyDB_shouldReturnZero():
    component_under_test = Einzelbuchungen()

    assert component_under_test.select().select_month(1).sum() == 0


def test_select_withMonthSelection_andNonMatchingMonth_shouldReturnZero():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('1.1.2011'), '', '', -10)

    assert component_under_test.select().select_month(2).sum() == 0


def test_group_by_kategorie__with_empty_db__should_return_empty_table():
    component_under_test = Einzelbuchungen()

    assert component_under_test.select().group_by_kategorie().empty


def test_group_by_kategorie():
    component_under_test = Einzelbuchungen()
    component_under_test.add(datum('20.01.1990'), 'A', '', -10)
    component_under_test.add(datum('20.01.1990'), 'A', '', -10)
    component_under_test.add(datum('20.01.1990'), 'B', '', 8)

    assert component_under_test.select().group_by_kategorie().Wert.tolist() == [-20, 8]
    assert component_under_test.select().group_by_kategorie().index.tolist() == ['A', 'B']

