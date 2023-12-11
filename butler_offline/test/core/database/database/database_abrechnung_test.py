from butler_offline.core import configuration_provider
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import viewcore
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.core.database import Database
import datetime


ABRECHNUNG = """Abrechnung vom 01.01.2010 (17.03.2017-17.03.2017)
########################################
 Ergebnis:
%Ergebnis%

Ausgaben von Partner           -10.00
Ausgaben von Test_User           0.00
--------------------------------------
Gesamt                         -10.00


########################################
 Gesamtausgaben pro Person 
########################################
 Datum      Kategorie    Name                    Wert
17.03.2017  some kategorie some name              -5.00


########################################
 Ausgaben von Partner
########################################
 Datum      Kategorie    Name                    Wert
17.03.2017  some kategorie some name             -10.00


########################################
 Ausgaben von Test_User
########################################
 Datum      Kategorie    Name                    Wert


#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-17,some kategorie,some name,-5.00,False
#######MaschinenimportEnd
"""

ABRECHNUNG_VERHAELTNIS = """Abrechnung vom 01.01.2010 (17.03.2017-17.03.2017)
########################################
 Ergebnis:
%Ergebnis%

Ausgaben von Partner          -100.00
Ausgaben von Test_User           0.00
--------------------------------------
Gesamt                        -100.00


########################################
 Ausgaben von Partner
########################################
 Datum      Kategorie    Name                    Wert
17.03.2017  some kategorie some name            -100.00


########################################
 Ausgaben von Test_User
########################################
 Datum      Kategorie    Name                    Wert


#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-17,some kategorie,some name,-30.00,False
#######MaschinenimportEnd
"""

ABRECHNUNG_VERHAELTNIS_OTHER = """Abrechnung vom 01.01.2010 (17.03.2017-17.03.2017)
########################################
 Ergebnis:
%Ergebnis%

Ausgaben von Partner          -100.00
Ausgaben von Test_User           0.00
--------------------------------------
Gesamt                        -100.00


########################################
 Ausgaben von Partner
########################################
 Datum      Kategorie    Name                    Wert
17.03.2017  some kategorie some name            -100.00


########################################
 Ausgaben von Test_User
########################################
 Datum      Kategorie    Name                    Wert


#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-17,some kategorie,some name,-50.00,False
2017-03-17,Ausgleich,Ausgleich,20.00,False
#######MaschinenimportEnd
"""

MIN_DATE = datum('17.03.2017')
MAX_DATE = datum('17.03.2017')
NOW = datetime.datetime.combine(MIN_DATE, datetime.time.min)


def test_abrechnen_should_add_einzelbuchungen():
    database = Database()
    database.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', 10, viewcore.name_of_partner())

    database.abrechnen(
        mindate=MAX_DATE,
        maxdate=MAX_DATE,
        filesystem=FileSystemStub(),
        now=NOW
    )

    assert database.einzelbuchungen.select().count() == 1
    uebertragene_buchung = database.einzelbuchungen.get(0)
    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '5.00'


def test_refresh_should_import_sparbuchungen():
    database = Database()
    database.sparbuchungen.add(datum('01.01.2020'), '1name', 123, database.sparbuchungen.TYP_MANUELLER_AUFTRAG, 'demokonto')

    database.refresh()

    assert len(database.einzelbuchungen.get_all()) == 1
    assert database.einzelbuchungen.get(0) == {'Datum': datum('01.01.2020'),
                                         'Dynamisch': True,
                                         'Kategorie': 'Sparen',
                                         'Name': '1name',
                                         'Tags': [],
                                         'Wert': -123,
                                         'index': 0}


def test_abrechnen_with_date_range_should_only_import_matching_elements():
    database = Database()
    database.gemeinsamebuchungen.add(datum('17.03.2010'), 'to early', 'to early', 99, viewcore.name_of_partner())
    database.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', 10, viewcore.name_of_partner())
    database.gemeinsamebuchungen.add(datum('17.03.2020'), 'to late', 'to late', 99, viewcore.name_of_partner())

    database.abrechnen(
        mindate=datum('01.01.2017'),
        maxdate=datum('01.12.2017'),
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('17.03.2017'), datetime.time.min)
    )

    assert database.einzelbuchungen.select().count() == 1
    uebertragene_buchung = database.einzelbuchungen.get(0)
    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '5.00'

    assert database.gemeinsamebuchungen.select().count() == 2
    uebertragene_buchung = database.gemeinsamebuchungen.select().to_list()[0]
    assert uebertragene_buchung['Name'] == 'to early'
    uebertragene_buchung = database.gemeinsamebuchungen.select().to_list()[1]
    assert uebertragene_buchung['Name'] == 'to late'


def test_abrechnen_with_date_range():
    configuration_provider.set_configuration('PARTNERNAME', 'Partner')

    database = Database(name='Test_User')
    database.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

    abrechnungs_text = database.abrechnen(
        mindate=MIN_DATE,
        maxdate=MAX_DATE,
        set_ergebnis='%Ergebnis%',
        verhaeltnis=70,
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('01.01.2010'), datetime.time.min)
    )

    assert database.einzelbuchungen.select().count() == 1
    uebertragene_buchung = database.einzelbuchungen.get(0)
    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '-70.00'

    assert abrechnungs_text == ABRECHNUNG_VERHAELTNIS


def test_abrechnen_with_self_kategorie_set_should_add_self_kategorie():
    configuration_provider.set_configuration('PARTNERNAME', 'Partner')
    database = Database(name='Test_User')
    database.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

    abrechnungs_text = database.abrechnen(
        mindate=MIN_DATE,
        maxdate=MAX_DATE,
        set_ergebnis='%Ergebnis%',
        verhaeltnis=70,
        set_self_kategorie='Ausgleich',
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('01.01.2010'), datetime.time.min)
    )

    assert database.einzelbuchungen.select().count() == 2

    if database.einzelbuchungen.get(0)['Name'] == 'Ausgleich':
        uebertragene_buchung = database.einzelbuchungen.get(1)
        ausgleichsbuchung = database.einzelbuchungen.get(0)
    else:
        uebertragene_buchung = database.einzelbuchungen.get(0)
        ausgleichsbuchung = database.einzelbuchungen.get(1)

    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '-50.00'

    assert ausgleichsbuchung['Name'] == 'Ausgleich'
    assert ausgleichsbuchung['Datum'] == datum('17.03.2017')
    assert ausgleichsbuchung['Kategorie'] == 'Ausgleich'
    assert ausgleichsbuchung['Wert'] == '-20.00'

    assert abrechnungs_text == ABRECHNUNG_VERHAELTNIS


def test_abrechnen_with_self_kategorie_set_should_add_self_kategorie_inverse():
    database = Database('Test_User')
    database.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

    database.abrechnen(
        mindate=datum('17.03.2017'),
        maxdate=datum('17.03.2017'),
        set_ergebnis='%Ergebnis%',
        verhaeltnis=30,
        set_self_kategorie='Ausgleich',
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('01.01.2010'), datetime.time.min)
    )

    assert database.einzelbuchungen.select().count() == 2

    if database.einzelbuchungen.get(0)['Name'] == 'Ausgleich':
        uebertragene_buchung = database.einzelbuchungen.get(1)
        ausgleichsbuchung = database.einzelbuchungen.get(0)
    else:
        uebertragene_buchung = database.einzelbuchungen.get(0)
        ausgleichsbuchung = database.einzelbuchungen.get(1)

    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '-50.00'

    assert ausgleichsbuchung['Name'] == 'Ausgleich'
    assert ausgleichsbuchung['Datum'] == datum('17.03.2017')
    assert ausgleichsbuchung['Kategorie'] == 'Ausgleich'
    assert ausgleichsbuchung['Wert'] == '20.00'


def test_abrechnen_with_other_kategorie_set_should_add_other_kategorie():
    configuration_provider.set_configuration('PARTNERNAME', 'Partner')
    database = Database('Test_User')
    database.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

    abrechnungs_text = database.abrechnen(
        mindate=datum('17.03.2017'),
        maxdate=datum('17.03.2017'),
        set_ergebnis='%Ergebnis%',
        verhaeltnis=70,
        set_other_kategorie='Ausgleich',
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('01.01.2010'), datetime.time.min)
    )

    assert database.einzelbuchungen.select().count() == 1

    uebertragene_buchung = database.einzelbuchungen.get(0)

    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '-70.00'

    assert abrechnungs_text == ABRECHNUNG_VERHAELTNIS_OTHER


def test_abrechnen_should_print_file_content():
    configuration_provider.set_configuration('PARTNERNAME', 'Partner')
    database = Database(name='Test_User')
    database.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -10, viewcore.name_of_partner())
    abrechnungs_text = database.abrechnen(
        mindate=datum('17.03.2017'),
        maxdate=datum('17.03.2017'),
        set_ergebnis='%Ergebnis%',
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('01.01.2010'), datetime.time.min)
    )

    assert abrechnungs_text == ABRECHNUNG
