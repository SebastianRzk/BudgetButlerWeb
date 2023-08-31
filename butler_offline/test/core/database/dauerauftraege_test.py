from datetime import date

from butler_offline.core.database.dauerauftraege import Dauerauftraege
from butler_offline.core.frequency import FREQUENCY_MONATLICH_NAME, \
    FREQUENCY_VIERTELJAEHRLICH_NAME, \
    FREQUENCY_HALBJAEHRLICH_NAME, \
    FREQUENCY_JAEHRLICH_NAME
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.test.core.database import extract_name_column, extract_index


def test_add_should_taint():
    component_under_test = Dauerauftraege()
    assert component_under_test.taint_number() == 0
    component_under_test.add(
        datum('1.1.2010'),
        date.today(),
        'some kategorie',
        'some name',
        'some rhythmus',
        1.23)
    assert component_under_test.taint_number() == 1


def test_edit_should_taint():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        date.today(),
        'some kategorie',
        'some name',
        'some rhythmus',
        1.23)
    assert component_under_test.taint_number() == 1
    component_under_test.edit(
        0,
        datum('2.1.2010'),
        datum('3.1.2010'),
        'some other kategorie',
        'some other name',
        'some other rhythmus',
        2.34)
    assert component_under_test.taint_number() == 2


def test_add_should_sort_and_drop_index():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2020'),
        datum('1.1.2020'),
        'kategorie1',
        'name1',
        'rhythmus1',
        1.23)
    component_under_test.add(
        datum('1.1.2010'),
        datum('1.1.2010'),
        'kategorie2',
        'name2',
        'rhythmus2',
        1.23)

    assert extract_name_column(component_under_test) == ['name2', 'name1']
    assert extract_index(component_under_test) == [0, 1]


def test_edit_should_sort_and_drop_index():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        datum('1.1.2010'),
        'kategorie1',
        'name1',
        'rhythmus1',
        1.23)
    component_under_test.add(
        datum('1.1.2020'),
        datum('1.1.2020'),
        'kategorie2',
        'name2',
        'rhythmus2',
        1.23)

    component_under_test.edit(
        1,
        datum('1.1.2000'),
        datum('1.1.2000'),
        'kategorie2',
        'name2',
        'rhythmus2',
        1.23)

    assert extract_name_column(component_under_test) == ['name2', 'name1']
    assert extract_index(component_under_test) == [0, 1]


def test_delete_should_taint():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        date.today(),
        'some kategorie',
        'some name',
        'some rhythmus',
        1.23)
    assert component_under_test.taint_number() == 1
    component_under_test.delete(0)
    assert component_under_test.taint_number() == 2


def test_get():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        date.today(),
        'some kategorie',
        'some name',
        'some rhythmus',
        1.23)

    result = component_under_test.get(0)

    assert len(component_under_test.content) == 1
    assert result['Startdatum'] == datum('1.1.2010')
    assert result['Endedatum'] == date.today()
    assert result['Name'] == 'some name'
    assert result['Kategorie'] == 'some kategorie'
    assert result['Rhythmus'] == 'some rhythmus'
    assert result['Wert'] == 1.23


def test_add():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        date.today(),
        'some kategorie',
        'some name',
        'some rhythmus',
        1.23)

    assert len(component_under_test.content) == 1
    assert component_under_test.content.Startdatum[0] == datum('1.1.2010')
    assert component_under_test.content.Endedatum[0] == date.today()
    assert component_under_test.content.Name[0] == 'some name'
    assert component_under_test.content.Kategorie[0] == 'some kategorie'
    assert component_under_test.content.Rhythmus[0] == 'some rhythmus'
    assert component_under_test.content.Wert[0] == 1.23


def test_aendere_bei_leerer_datenbank():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        date.today(),
        'some kategorie',
        'some name',
        'some rhythmus',
        1.23)
    component_under_test.edit(
        0,
        datum('2.1.2010'),
        datum('3.1.2010'),
        'some other kategorie',
        'some other name',
        'some other rhythmus',
        2.34)

    assert len(component_under_test.content) == 1
    assert component_under_test.content.Startdatum[0] == datum('2.1.2010')
    assert component_under_test.content.Endedatum[0] == datum('3.1.2010')
    assert component_under_test.content.Name[0] == 'some other name'
    assert component_under_test.content.Kategorie[0] == 'some other kategorie'
    assert component_under_test.content.Rhythmus[0] == 'some other rhythmus'
    assert component_under_test.content.Wert[0] == 2.34


def test_aendere_bei_voller_datenbank():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        date.today(),
        '1some kategorie',
        '1some name',
        '1some rhythmus',
        1.23)
    component_under_test.add(
        datum('1.1.2011'),
        date.today(),
        '2some kategorie',
        '2some name',
        '2some rhythmus',
        1.23)
    component_under_test.add(
        datum('1.1.2012'),
        date.today(),
        '3some kategorie',
        '3some name',
        '3some rhythmus',
        1.23)

    component_under_test.edit(
        1,
        datum('2.1.2011'),
        datum('3.1.2011'),
        'some other kategorie',
        'some other name',
        'some other rhythmus',
        2.34)

    assert len(component_under_test.content) == 3
    assert component_under_test.content.Startdatum[1] == datum('2.1.2011')
    assert component_under_test.content.Endedatum[1] == datum('3.1.2011')
    assert component_under_test.content.Name[1] == 'some other name'
    assert component_under_test.content.Kategorie[1] == 'some other kategorie'
    assert component_under_test.content.Rhythmus[1] == 'some other rhythmus'
    assert component_under_test.content.Wert[1] == 2.34


def test_get_aktuelle_with_actual_dauerauftrag_should_return_dauerauftrag():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('01.01.2012'),
        datum('01.01.2100'),
        'some kategorie',
        'some name',
        'some rhythmus',
        1)

    result = component_under_test.aktuelle()

    assert len(result) == 1
    assert result[0]['Startdatum'] == datum('01.01.2012')
    assert result[0]['Endedatum'] == datum('01.01.2100')
    assert result[0]['Kategorie'] == 'some kategorie'
    assert result[0]['Name'] == 'some name'
    assert result[0]['Rhythmus'] == 'some rhythmus'
    assert result[0]['Wert'] == 1


def test_get_aktuelle_with_past_dauerauftrag_should_return_empty_list():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('01.01.2012'),
        datum('01.01.2012'),
        'some kategorie',
        'some name',
        'some rhythmus',
        1)

    result = component_under_test.aktuelle()

    assert result == []


def test_get_aktuelle_with_future_dauerauftrag_should_return_empty_list():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('01.01.2100'),
        datum('01.01.2100'),
        'some kategorie',
        'some name',
        'some rhythmus',
        1)

    result = component_under_test.aktuelle()

    assert result == []


def test_get_past_with_past_dauerauftrag_should_return_dauerauftrag():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('01.01.2012'),
        datum('01.01.2012'),
        'some kategorie',
        'some name',
        'some rhythmus',
        1)

    result = component_under_test.past()

    assert len(result) == 1
    assert result[0]['Startdatum'] == datum('01.01.2012')
    assert result[0]['Endedatum'] == datum('01.01.2012')
    assert result[0]['Kategorie'] == 'some kategorie'
    assert result[0]['Name'] == 'some name'
    assert result[0]['Rhythmus'] == 'some rhythmus'
    assert result[0]['Wert'] == 1


def test_get_past_with_actual_dauerauftrag_should_return_empty_list():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('01.01.2012'),
        datum('01.01.2100'),
        'some kategorie',
        'some name',
        'some rhythmus',
        1)

    result = component_under_test.past()

    assert result == []


def test_get_future_with_actual_dauerauftrag_should_return_empty():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('01.01.2012'),
        datum('01.01.2100'),
        'some kategorie',
        'some name',
        'some rhythmus',
        1)

    result = component_under_test.future()

    assert result == []


def test_get_future_with_future_dauerauftrag_should_return_dauerauftrag():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('01.01.2100'),
        datum('01.01.2100'),
        'some kategorie',
        'some name',
        'some rhythmus',
        1)

    result = component_under_test.future()

    assert len(result) == 1
    assert result[0]['Startdatum'] == datum('01.01.2100')
    assert result[0]['Endedatum'] == datum('01.01.2100')
    assert result[0]['Kategorie'] == 'some kategorie'
    assert result[0]['Name'] == 'some name'
    assert result[0]['Rhythmus'] == 'some rhythmus'
    assert result[0]['Wert'] == 1


def test_get_einzelbuchungen_until_today():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        datum('2.2.2010'),
        'some kategorie',
        'some name',
        FREQUENCY_MONATLICH_NAME,
        1.23)

    result = component_under_test.get_all_einzelbuchungen_until_today()

    assert len(result) == 2
    first_row = result.iloc[0]
    assert first_row.Datum == datum('1.1.2010')
    assert first_row.Kategorie == 'some kategorie'
    assert first_row.Name == 'some name'
    assert first_row.Wert == 1.23

    second_row = result.iloc[1]
    assert second_row.Datum == datum('1.2.2010')
    assert second_row.Kategorie == 'some kategorie'
    assert second_row.Name == 'some name'
    assert second_row.Wert == 1.23


def test_get_einzelbuchungen_until_today_quarterly():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        datum('2.4.2010'),
        'some kategorie',
        'some name',
        FREQUENCY_VIERTELJAEHRLICH_NAME,
        1.23)

    result = component_under_test.get_all_einzelbuchungen_until_today()

    assert len(result) == 2
    first_row = result.iloc[0]
    assert first_row.Datum == datum('1.1.2010')
    assert first_row.Kategorie == 'some kategorie'
    assert first_row.Name == 'some name'
    assert first_row.Wert == 1.23

    second_row = result.iloc[1]
    assert second_row.Datum == datum('1.4.2010')
    assert second_row.Kategorie == 'some kategorie'
    assert second_row.Name == 'some name'
    assert second_row.Wert == 1.23


def test_get_einzelbuchungen_until_half_yearly():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        datum('2.7.2010'),
        'some kategorie',
        'some name',
        FREQUENCY_HALBJAEHRLICH_NAME,
        1.23)

    result = component_under_test.get_all_einzelbuchungen_until_today()

    assert len(result) == 2
    first_row = result.iloc[0]
    assert first_row.Datum == datum('1.1.2010')
    assert first_row.Kategorie == 'some kategorie'
    assert first_row.Name == 'some name'
    assert first_row.Wert == 1.23

    second_row = result.iloc[1]
    assert second_row.Datum == datum('1.7.2010')
    assert second_row.Kategorie == 'some kategorie'
    assert second_row.Name == 'some name'
    assert second_row.Wert == 1.23


def test_get_einzelbuchungen_until_yearly():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('1.1.2010'),
        datum('2.1.2011'),
        'some kategorie',
        'some name',
        FREQUENCY_JAEHRLICH_NAME,
        1.23)

    result = component_under_test.get_all_einzelbuchungen_until_today()

    assert len(result) == 2
    first_row = result.iloc[0]
    assert first_row.Datum == datum('1.1.2010')
    assert first_row.Kategorie == 'some kategorie'
    assert first_row.Name == 'some name'
    assert first_row.Wert == 1.23

    second_row = result.iloc[1]
    assert second_row.Datum == datum('1.1.2011')
    assert second_row.Kategorie == 'some kategorie'
    assert second_row.Name == 'some name'
    assert second_row.Wert == 1.23


def test_get_einzelbuchungen_until_today_should_use_end_of_month_when_overflow():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('31.1.2010'),
        datum('2.3.2010'),
        'some kategorie',
        'some name',
        FREQUENCY_MONATLICH_NAME,
        1.23)

    result = component_under_test.get_all_einzelbuchungen_until_today()

    assert len(result) == 2
    first_row = result.iloc[0]
    assert first_row.Datum == datum('31.1.2010')
    assert first_row.Kategorie == 'some kategorie'
    assert first_row.Name == 'some name'
    assert first_row.Wert == 1.23

    second_row = result.iloc[1]
    assert second_row.Datum == datum('28.2.2010')
    assert second_row.Kategorie == 'some kategorie'
    assert second_row.Name == 'some name'
    assert second_row.Wert == 1.23


def test_get_all_einzelbuchungen_until_today_should_return_element_with_empty_tag_list():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        datum('31.1.2010'),
        datum('2.2.2010'),
        'some kategorie',
        'some name',
        FREQUENCY_MONATLICH_NAME,
        1.23)

    result = component_under_test.get_all_einzelbuchungen_until_today()

    row = result.iloc[0]

    assert row.Datum == datum('31.1.2010')
    assert row.Kategorie == 'some kategorie'
    assert row.Name == 'some name'
    assert row.Wert == 1.23
    assert row.Dynamisch
    assert row.Tags == []


def test_sort_columns_should_be_containing_all_values_of_read_columns_to_prevent_edit_instabilities():
    component_under_test = Dauerauftraege()

    assert set(component_under_test.TABLE_HEADER) == set(component_under_test.SORT_ORDER)


def test_rename_should_rename():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        any_datum_1(),
        any_datum_2(),
        'kategorie1',
        'some name3',
        FREQUENCY_MONATLICH_NAME,
        1.23)
    component_under_test.add(
        any_datum_3(),
        any_datum_4(),
        'kategorie2',
        'some name3',
        FREQUENCY_MONATLICH_NAME,
        1.23)
    component_under_test.add(
        any_datum_5(),
        any_datum_6(),
        'kategorie3',
        'some name3',
        FREQUENCY_MONATLICH_NAME,
        1.23)

    element1 = {'Endedatum': any_datum_2(),
                'Kategorie': 'kategorie1',
                'Name': 'some name3',
                'Rhythmus': 'monatlich',
                'Startdatum': any_datum_1(),
                'Wert': 1.23,
                'index': 0}
    element2 = {'Endedatum': any_datum_4(),
                'Kategorie': 'kategorie2',
                'Name': 'some name3',
                'Rhythmus': 'monatlich',
                'Startdatum': any_datum_3(),
                'Wert': 1.23,
                'index': 1}
    element3 = {'Endedatum': any_datum_6(),
                'Kategorie': 'kategorie3',
                'Name': 'some name3',
                'Rhythmus': 'monatlich',
                'Startdatum': any_datum_5(),
                'Wert': 1.23,
                'index': 2}
    assert component_under_test.select().to_list() == [element1, element2, element3]

    component_under_test.rename_kategorie(alter_name='kategorie2', neuer_name='kategorie4')

    assert component_under_test.select().to_list() == [element1,
                                                       {'Endedatum': any_datum_4(),
                                                        'Kategorie': 'kategorie4',
                                                        'Name': 'some name3',
                                                        'Rhythmus': 'monatlich',
                                                        'Startdatum': any_datum_3(),
                                                        'Wert': 1.23,
                                                        'index': 1},
                                                       element3]
    assert component_under_test.tainted


def test_rename_should_resort():
    component_under_test = Dauerauftraege()
    component_under_test.add(
        any_datum_1(),
        any_datum_2(),
        'kategorie1',
        'some name3',
        FREQUENCY_MONATLICH_NAME,
        1.23)
    component_under_test.add(
        any_datum_1(),
        any_datum_2(),
        'kategorie2',
        'some name3',
        FREQUENCY_MONATLICH_NAME,
        1.23)
    element1 = {'Endedatum': any_datum_2(),
                'Kategorie': 'kategorie1',
                'Name': 'some name3',
                'Rhythmus': 'monatlich',
                'Startdatum': any_datum_1(),
                'Wert': 1.23,
                'index': 0}
    element2 = {'Endedatum': any_datum_2(),
                'Kategorie': 'kategorie2',
                'Name': 'some name3',
                'Rhythmus': 'monatlich',
                'Startdatum': any_datum_1(),
                'Wert': 1.23,
                'index': 1}
    assert component_under_test.select().to_list() == [element1, element2]

    component_under_test.rename_kategorie(alter_name='kategorie2', neuer_name='kategorie0')

    assert component_under_test.select().to_list() == [{'Endedatum': any_datum_2(),
                                                        'Kategorie': 'kategorie0',
                                                        'Name': 'some name3',
                                                        'Rhythmus': 'monatlich',
                                                        'Startdatum': any_datum_1(),
                                                        'Wert': 1.23,
                                                        'index': 1} | {'index': 0},
                                                       element1 | {'index': 1}]


def any_datum_6():
    return datum('2.2.2013')


def any_datum_5():
    return datum('31.1.2012')


def any_datum_4():
    return datum('2.2.2011')


def any_datum_3():
    return datum('31.1.2011')


def any_datum_2():
    return datum('2.2.2010')


def any_datum_1():
    return datum('31.1.2010')
