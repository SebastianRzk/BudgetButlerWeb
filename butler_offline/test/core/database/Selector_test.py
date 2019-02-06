import unittest
from datetime import date

from butler_offline.core.database.Einzelbuchungen import Einzelbuchungen
from butler_offline.viewcore.converter import datum_from_german as datum


class SelectorTest(unittest.TestCase):

    def test_inject_zeroes_for_year_and_kategories_shouldInjectZeroes(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.02.2017'), 'kat1', '', 5,)
        component_under_test.add(datum('01.02.2017'), 'kat2', '', 5,)
        result = component_under_test.select().inject_zeroes_for_year_and_kategories(2017).raw_table()
        assert len(result) == 26
        assert datum('01.01.2017') in set(result.Datum)
        assert datum('01.12.2017') in set(result.Datum)
        assert result.Wert.sum() == 10
        assert set(['kat1', 'kat2']) == set(result.Kategorie)

    def test_sum_kategorien_monthly(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.02.2017'), 'kat1', '', 5,)
        component_under_test.add(datum('01.02.2017'), 'kat2', '', 10,)
        result = component_under_test.select().sum_kategorien_monthly()
        assert len(result) == 1
        assert len(result[2]) == 2
        assert result[2]['kat1'] == '5.00'
        assert result[2]['kat2'] == '10.00'

    def test_inject_zeroes_for_year_and_kategories_wothNoValues_shouldInjectZeroes(self):
        component_under_test = Einzelbuchungen()
        assert component_under_test.select().inject_zeroes_for_year_and_kategories(2017).sum() == 0


    def test_injectZeros_shouldInjectZeroes(self):
        component_under_test = Einzelbuchungen()
        select = component_under_test.select()

        assert len(select.content) == 0

        select = select.inject_zeros_for_year(2017)
        assert len(select.content) == 12
        assert select.content.loc[0].Datum == datum('01.01.2017')
        assert select.content.loc[11].Datum == datum('01.12.2017')
        assert select.content.Wert.sum() == 0

    def test_sumMonthly_withUniqueMonths(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.01.2017'), '', '', 20,)
        component_under_test.add(datum('01.02.2017'), '', '', 10,)

        result = component_under_test.select().sum_monthly()

        assert result == ['20.00', '10.00']

    def test_sumMonthly_withDuplicatedMonths_shouldSumValues(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01.02.2017'), '', '', 5,)
        component_under_test.add(datum('01.01.2017'), '', '', 20,)
        component_under_test.add(datum('01.02.2017'), '', '', 10,)

        result = component_under_test.select().sum_monthly()

        assert result == ['20.00', '15.00']

    def test_sum_withEmptyDB_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()
        assert component_under_test.select().sum() == 0

    def test_sum_withBuchung_shouldReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2010'), '', '', 10)

        assert component_under_test.select().sum() == 10

    def test_filterYear_withNonMatchingYear_shouldRemoveItem(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2010'), '', '', 10)

        assert component_under_test.select().select_year(2011).sum() == 0

    def test_filterYear_withMatchingYear_shoudReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', 10)

        assert component_under_test.select().select_year(2011).sum() == 10

    def test_einnahmen_withEinnahme_shoudReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', 10)

        assert component_under_test.select().select_einnahmen().select_year(2011).sum() == 10

    def test_einnahmen_withAusgabe_shoudReturnZero(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', -10)

        assert component_under_test.select().select_einnahmen().select_year(2011).sum() == 0

    def test_ausgaben_withEinnahme_shoudReturnZero(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', 10)

        assert component_under_test.select().select_ausgaben().select_year(2011).sum() == 0

    def test_ausgaben_withAusgabe_shoudReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', -10)

        assert component_under_test.select().select_ausgaben().select_year(2011).sum() == -10

    def test_select_withMonthSelection_andMatchingMonth_shouldReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', -10)

        assert component_under_test.select().select_month(1).sum() == -10

    def test_select_withMonthSelection_andEmptyDB_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()

        assert component_under_test.select().select_month(1).sum() == 0

    def test_select_withMonthSelection_andNonMatchingMonth_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('1.1.2011'), '', '', -10)

        assert component_under_test.select().select_month(2).sum() == 0

    def test_select_withThisMonthSelection_andMatchingMonth_shouldReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), '', '', -10)

        assert component_under_test.select().select_aktueller_monat().sum() == -10

    def test_select_withThisMonthSelection_andNonMatchingDate_shouldReturnValue(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('20.01.1990'), '', '', -10)

        assert component_under_test.select().select_aktueller_monat().sum() == 0

    def test_group_by_kategorie_withEmptyDB_shouldReturnEmptyTable(self):
        component_under_test = Einzelbuchungen()

        assert component_under_test.select().group_by_kategorie().empty

    def test_group_by_kategorie_shouldGroupValues(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('20.01.1990'), 'A', '', -10)
        component_under_test.add(datum('20.01.1990'), 'A', '', -10)
        component_under_test.add(datum('20.01.1990'), 'B', '', 8)

        assert component_under_test.select().group_by_kategorie().Wert.tolist() == [-20, 8]
        assert component_under_test.select().group_by_kategorie().index.tolist() == ['A', 'B']

from butler_offline.core.database.Gemeinsamebuchungen import Gemeinsamebuchungen

class GemeinsamSelectorTest(unittest.TestCase):
    def test_selectRange_withEntriesContainigMatchingDates_shouldReturnEntries(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('01.01.2010'),
            'some kategorie',
            'some name',
            1.23,
            'sebastian')

        assert component_under_test.select().select_range(datum('01.01.2009'), datum('01.01.2011')).to_list() == [{
            'Datum': datum('01.01.2010'),
            'Kategorie': 'some kategorie',
            'Name': 'some name',
            'Wert': 1.23,
            'Person': 'sebastian',
            'index': 0
        }]

    def test_selectRange_withOutOfRangeEntries_shouldFilterThemOut(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('01.01.2010'),
            'some kategorie',
            'some name',
            1.23,
            'sebastian')
        component_under_test.add(
            datum('01.01.2000'),
            'xxxx',
            'xxxx',
            0.00,
            'xxxx')
        component_under_test.add(
            datum('01.01.2020'),
            'yyyy',
            'yyyy',
            0.00,
            'yyyy')

        assert component_under_test.select().select_range(datum('01.01.2009'), datum('01.01.2011')).to_list() == [{
            'Datum': datum('01.01.2010'),
            'Kategorie': 'some kategorie',
            'Name': 'some name',
            'Wert': 1.23,
            'Person': 'sebastian',
            'index': 1
        }]
