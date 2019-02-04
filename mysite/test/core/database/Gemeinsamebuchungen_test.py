'''
Created on 11.08.2017

@author: sebastian
'''
import unittest

from mysite.viewcore.converter import datum_from_german as datum
from mysite.core.database.Gemeinsamebuchungen import Gemeinsamebuchungen

class gemeinsame_buchungen(unittest.TestCase):

    def test_add_shouldTaint(self):
        component_under_test = Gemeinsamebuchungen()
        assert component_under_test.taint_number() == 0
        component_under_test.add(
            datum('1.1.2010'),
            'some kategorie',
            'some name',
            1.23,
            'sebastian')
        assert component_under_test.taint_number() == 1

    def test_edit_shouldTaint(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('1.1.2010'),
            'some kategorie',
            'some name',
            1.23,
            'sebastian')
        component_under_test.de_taint()
        assert component_under_test.taint_number() == 0
        component_under_test.edit(
            0,
            datum('2.1.2010'),
            'some other kategorie',
            'some other name',
            2.34,
            'sebastian')
        assert component_under_test.taint_number() == 1

    def test_edit_shouldEdit(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('1.1.2011'),
            'yyName',
            'yyKategorie',
            1.23,
            'sebastian')
        component_under_test.de_taint()
        assert component_under_test.taint_number() == 0
        component_under_test.edit(
            0,
            datum('2.2.2012'),
            'zzName',
            'zzKategorie',
            2.34,
            'sebastian')
        assert component_under_test.get(0) == {
            'index': 0,
            'Datum': datum('2.2.2012'),
            'Kategorie': 'zzKategorie',
            'Name': 'zzName',
            'Wert': 2.34,
            'Person': 'sebastian'}

    def test_delete_shouldTaint(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('1.1.2010'),
            'some kategorie',
            'some name',
            1.23,
            'sebastian')
        component_under_test.de_taint()
        assert component_under_test.taint_number() == 0
        component_under_test.delete(0)
        assert component_under_test.taint_number() == 1

    def test_rename_shouldTaint(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('1.1.2010'),
            'some kategorie',
            'some name',
            1.23,
            'sebastian')
        component_under_test.de_taint()
        assert component_under_test.taint_number() == 0
        component_under_test.rename('sebastian', 'sebastian2')
        assert component_under_test.taint_number() == 1

    def test_selectRange_withEntriesContainigMatchingDates_shouldReturnEntries(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('01.01.2010'),
            'some kategorie',
            'some name',
            1.23,
            'sebastian')

        assert component_under_test.select_range(datum('01.01.2009'), datum('01.01.2011')).get_content() == [{
            'Datum': datum('01.01.2010'),
            'Kategorie': 'some kategorie',
            'Name': 'some name',
            'Wert': 1.23,
            'Person': 'sebastian'
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

        assert component_under_test.select_range(datum('01.01.2009'), datum('01.01.2011')).get_content() == [{
            'Datum': datum('01.01.2010'),
            'Kategorie': 'some kategorie',
            'Name': 'some name',
            'Wert': 1.23,
            'Person': 'sebastian'
        }]


    def test_drop_withMatchingIndex_shouldRemoveData(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('1.1.2010'),
            'kategorie1',
            'name1',
            1.23,
            'person1')

        component_under_test.add(
            datum('2.2.2020'),
            'kategorie2',
            'name2',
            3.45,
            'person2')

        component_under_test.drop([1])

        assert component_under_test.get_content() == [
            {
                'Datum': datum('01.01.2010'),
                'Kategorie': 'kategorie1',
                'Name': 'name1',
                'Person': 'person1',
                'Wert': 1.23
            }
        ]

    def test_drop_withNoMatchingIndex_shouldRemoveNothing(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('1.1.2010'),
            'kategorie1',
            'name1',
            1.23,
            'person1')

        component_under_test.add(
            datum('2.2.2020'),
            'kategorie2',
            'name2',
            3.45,
            'person2')

        component_under_test.drop([])

        assert component_under_test.get_content() == [
            {
                'Datum': datum('01.01.2010'),
                'Kategorie': 'kategorie1',
                'Name': 'name1',
                'Person': 'person1',
                'Wert': 1.23
            },
            {
                'Datum': datum('02.02.2020'),
                'Kategorie': 'kategorie2',
                'Name': 'name2',
                'Person': 'person2',
                'Wert': 3.45
            }
        ]


    def test_getContent_withNoEntry_shouldReturnEmptyList(self):
        component_under_test = Gemeinsamebuchungen()

        assert component_under_test.get_content() == []

    def test_getContent_withEntries_shouldReturnListOfDicts(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('1.1.2010'),
            'kategorie1',
            'name1',
            1.23,
            'person1')

        component_under_test.add(
            datum('2.2.2020'),
            'kategorie2',
            'name2',
            3.45,
            'person2')

        assert component_under_test.get_content() == [
            {
                'Datum': datum('01.01.2010'),
                'Kategorie': 'kategorie1',
                'Name': 'name1',
                'Person': 'person1',
                'Wert': 1.23
            },
            {
                'Datum': datum('02.02.2020'),
                'Kategorie': 'kategorie2',
                'Name': 'name2',
                'Person': 'person2',
                'Wert': 3.45
            }
        ]
