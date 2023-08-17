from butler_offline.core import configuration_provider
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import viewcore
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.core.database import Database
import datetime


abrechnung = """Abrechnung vom 01.01.2010 (17.03.2017-17.03.2017)
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

abrechnung_verhaeltnis = """Abrechnung vom 01.01.2010 (17.03.2017-17.03.2017)
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

abrechnung_verhaeltnis_other = """Abrechnung vom 01.01.2010 (17.03.2017-17.03.2017)
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


def test_abrechnen_should_add_einzelbuchungen():
    db = Database()
    db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', 10, viewcore.name_of_partner())

    db.abrechnen(
        mindate=datum('17.03.2017'),
        maxdate=datum('17.03.2017'),
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('17.03.2017'), datetime.time.min)
    )

    assert len(db.einzelbuchungen.content) == 1
    uebertragene_buchung = db.einzelbuchungen.get(0)
    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '5.00'


def test_refresh_should_import_sparbuchungen():
    db = Database()
    db.sparbuchungen.add(datum('01.01.2020'), '1name', 123, db.sparbuchungen.TYP_MANUELLER_AUFTRAG, 'demokonto')

    db.refresh()

    assert len(db.einzelbuchungen.get_all()) == 1
    assert db.einzelbuchungen.get(0) == {'Datum': datum('01.01.2020'),
                                         'Dynamisch': True,
                                         'Kategorie': 'Sparen',
                                         'Name': '1name',
                                         'Tags': [],
                                         'Wert': -123,
                                         'index': 0}


def test_abrechnen_with_date_range_should_only_import_matching_elements():
    db = Database()
    db.gemeinsamebuchungen.add(datum('17.03.2010'), 'to early', 'to early', 99, viewcore.name_of_partner())
    db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', 10, viewcore.name_of_partner())
    db.gemeinsamebuchungen.add(datum('17.03.2020'), 'to late', 'to late', 99, viewcore.name_of_partner())

    db.abrechnen(
        mindate=datum('01.01.2017'),
        maxdate=datum('01.12.2017'),
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('17.03.2017'), datetime.time.min)
    )

    assert len(db.einzelbuchungen.content) == 1
    uebertragene_buchung = db.einzelbuchungen.get(0)
    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '5.00'

    assert len(db.gemeinsamebuchungen.select().to_list()) == 2
    uebertragene_buchung = db.gemeinsamebuchungen.select().to_list()[0]
    assert uebertragene_buchung['Name'] == 'to early'
    uebertragene_buchung = db.gemeinsamebuchungen.select().to_list()[1]
    assert uebertragene_buchung['Name'] == 'to late'


def test_abrechnen_with_date_range():
    configuration_provider.set_configuration('PARTNERNAME', 'Partner')

    db = Database(name='Test_User')
    db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

    abrechnungs_text = db.abrechnen(
        mindate=datum('17.03.2017'),
        maxdate=datum('17.03.2017'),
        set_ergebnis='%Ergebnis%',
        verhaeltnis=70,
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('01.01.2010'), datetime.time.min)
    )

    assert len(db.einzelbuchungen.content) == 1
    uebertragene_buchung = db.einzelbuchungen.get(0)
    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '-70.00'

    assert abrechnungs_text == abrechnung_verhaeltnis


def test_abrechnen_with_self_kategorie_set_should_add_self_kategorie():
    configuration_provider.set_configuration('PARTNERNAME', 'Partner')
    db = Database(name='Test_User')
    db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

    abrechnungs_text = db.abrechnen(
        mindate=datum('17.03.2017'),
        maxdate=datum('17.03.2017'),
        set_ergebnis='%Ergebnis%',
        verhaeltnis=70,
        set_self_kategorie='Ausgleich',
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('01.01.2010'), datetime.time.min)
    )

    assert len(db.einzelbuchungen.content) == 2

    if db.einzelbuchungen.get(0)['Name'] == 'Ausgleich':
        uebertragene_buchung = db.einzelbuchungen.get(1)
        ausgleichsbuchung = db.einzelbuchungen.get(0)
    else:
        uebertragene_buchung = db.einzelbuchungen.get(0)
        ausgleichsbuchung = db.einzelbuchungen.get(1)

    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '-50.00'

    assert ausgleichsbuchung['Name'] == 'Ausgleich'
    assert ausgleichsbuchung['Datum'] == datum('17.03.2017')
    assert ausgleichsbuchung['Kategorie'] == 'Ausgleich'
    assert ausgleichsbuchung['Wert'] == '-20.00'

    assert abrechnungs_text == abrechnung_verhaeltnis


def test_abrechnen_with_self_kategorie_set_should_add_self_kategorie_inverse():
    db = Database('Test_User')
    db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

    db.abrechnen(
        mindate=datum('17.03.2017'),
        maxdate=datum('17.03.2017'),
        set_ergebnis='%Ergebnis%',
        verhaeltnis=30,
        set_self_kategorie='Ausgleich',
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('01.01.2010'), datetime.time.min)
    )

    assert len(db.einzelbuchungen.content) == 2

    if db.einzelbuchungen.get(0)['Name'] == 'Ausgleich':
        uebertragene_buchung = db.einzelbuchungen.get(1)
        ausgleichsbuchung = db.einzelbuchungen.get(0)
    else:
        uebertragene_buchung = db.einzelbuchungen.get(0)
        ausgleichsbuchung = db.einzelbuchungen.get(1)

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
    db = Database('Test_User')
    db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

    abrechnungs_text = db.abrechnen(
        mindate=datum('17.03.2017'),
        maxdate=datum('17.03.2017'),
        set_ergebnis='%Ergebnis%',
        verhaeltnis=70,
        set_other_kategorie='Ausgleich',
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('01.01.2010'), datetime.time.min)
    )

    assert len(db.einzelbuchungen.content) == 1

    uebertragene_buchung = db.einzelbuchungen.get(0)

    assert uebertragene_buchung['Name'] == 'some name'
    assert uebertragene_buchung['Datum'] == datum('17.03.2017')
    assert uebertragene_buchung['Kategorie'] == 'some kategorie'
    assert uebertragene_buchung['Wert'] == '-70.00'

    assert abrechnungs_text == abrechnung_verhaeltnis_other


def test_abrechnen_should_print_file_content():
    configuration_provider.set_configuration('PARTNERNAME', 'Partner')
    db = Database(name='Test_User')
    db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -10, viewcore.name_of_partner())
    abrechnungs_text = db.abrechnen(
        mindate=datum('17.03.2017'),
        maxdate=datum('17.03.2017'),
        set_ergebnis='%Ergebnis%',
        filesystem=FileSystemStub(),
        now=datetime.datetime.combine(datum('01.01.2010'), datetime.time.min)
    )

    assert abrechnungs_text == abrechnung
