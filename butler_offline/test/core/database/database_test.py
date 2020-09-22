'''
Created on 10.05.2017

@author: sebastian
'''

import unittest
from pandas import DataFrame

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.core import file_system
from butler_offline.core.database import Database
from butler_offline.core import time
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import viewcore
from butler_offline.viewcore import configuration_provider
from butler_offline.viewcore.state import persisted_state


class abrechnen(unittest.TestCase):
    abrechnung = """Abrechnung vom 01.01.2010 (17.03.2017-17.03.2017)
########################################
 Ergebnis:
%Ergebnis%

Ausgaben von Maureen           -10.00
Ausgaben von Test_User           0.00
--------------------------------------
Gesamt                         -10.00


########################################
 Gesamtausgaben pro Person 
########################################
 Datum      Kategorie    Name                    Wert
17.03.2017  some kategorie some name              -5.00


########################################
 Ausgaben von Maureen
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

    abrechnung_verhaeltnis =  """Abrechnung vom 01.01.2010 (17.03.2017-17.03.2017)
########################################
 Ergebnis:
%Ergebnis%

Ausgaben von Maureen          -100.00
Ausgaben von Test_User           0.00
--------------------------------------
Gesamt                        -100.00


########################################
 Ausgaben von Maureen
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

Ausgaben von Maureen          -100.00
Ausgaben von Test_User           0.00
--------------------------------------
Gesamt                        -100.00


########################################
 Ausgaben von Maureen
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

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        persisted_state.DATABASES = []
        configuration_provider.set_configuration('PARTNERNAME', 'Maureen')

    def test_abrechnen_shouldAddEinzelbuchungen(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', 10, viewcore.name_of_partner())

        db.abrechnen()

        assert len(db.einzelbuchungen.content) == 1
        uebertragene_buchung = db.einzelbuchungen.get(0)
        assert uebertragene_buchung['Name'] == 'some name'
        assert uebertragene_buchung['Datum'] == datum('17.03.2017')
        assert uebertragene_buchung['Kategorie'] == 'some kategorie'
        assert uebertragene_buchung['Wert'] == '5.00'

    def test_refresh_shouldImport_sparbuchungen(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.sparbuchungen.add(datum('01.01.2020'), '1name', 123, db.sparbuchungen.TYP_MANUELLER_AUFTRAG, 'demokonto')

        db.refresh()

        assert len(db.einzelbuchungen.get_all()) == 1
        assert db.einzelbuchungen.get(0) == {'Datum': datum('01.01.2020'),
                                             'Dynamisch': True,
                                             'Kategorie': 'Sparen',
                                             'Name': '1name',
                                             'Tags': None,
                                             'Wert': -123,
                                             'index': 0}

    def test_abrechnen_withDateRange_shouldOnlyImportMatchingElements(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.gemeinsamebuchungen.add(datum('17.03.2010'), 'to early', 'to early', 99, viewcore.name_of_partner())
        db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', 10, viewcore.name_of_partner())
        db.gemeinsamebuchungen.add(datum('17.03.2020'), 'to late', 'to late', 99, viewcore.name_of_partner())

        db.abrechnen(mindate=datum('01.01.2017'), maxdate=datum('01.12.2017'))

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

    def test_abrechnen_withDateRange(self):
        self.set_up()
        db = persisted_state.database_instance()
        time.stub_today_with(datum('01.01.2010'))
        db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

        abrechnungs_text = db.abrechnen(set_ergebnis='%Ergebnis%', verhaeltnis=70)

        assert len(db.einzelbuchungen.content) == 1
        uebertragene_buchung = db.einzelbuchungen.get(0)
        assert uebertragene_buchung['Name'] == 'some name'
        assert uebertragene_buchung['Datum'] == datum('17.03.2017')
        assert uebertragene_buchung['Kategorie'] == 'some kategorie'
        assert uebertragene_buchung['Wert'] == '-70.00'

        assert abrechnungs_text == self.abrechnung_verhaeltnis


    def test_abrechnen_withSelfKategorieSet_shouldAddSelfKategorie(self):
        self.set_up()
        db = persisted_state.database_instance()
        time.stub_today_with(datum('01.01.2010'))
        db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

        abrechnungs_text = db.abrechnen(set_ergebnis='%Ergebnis%', verhaeltnis=70, set_self_kategorie='Ausgleich')

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

        uebertragene_buchung = db.einzelbuchungen.get(1)
        assert ausgleichsbuchung['Name'] == 'Ausgleich'
        assert ausgleichsbuchung['Datum'] == datum('17.03.2017')
        assert ausgleichsbuchung['Kategorie'] == 'Ausgleich'
        assert ausgleichsbuchung['Wert'] == '-20.00'

        assert abrechnungs_text == self.abrechnung_verhaeltnis


    def test_abrechnen_withSelfKategorieSet_shouldAddSelfKategorie_inverse(self):
        self.set_up()
        db = persisted_state.database_instance()
        time.stub_today_with(datum('01.01.2010'))
        db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

        abrechnungs_text = db.abrechnen(set_ergebnis='%Ergebnis%', verhaeltnis=30, set_self_kategorie='Ausgleich')

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

        uebertragene_buchung = db.einzelbuchungen.get(1)
        assert ausgleichsbuchung['Name'] == 'Ausgleich'
        assert ausgleichsbuchung['Datum'] == datum('17.03.2017')
        assert ausgleichsbuchung['Kategorie'] == 'Ausgleich'
        assert ausgleichsbuchung['Wert'] == '20.00'



    def test_abrechnen_withOtherKategorieSet_shouldAddOtherKategorie(self):
        self.set_up()
        db = persisted_state.database_instance()
        time.stub_today_with(datum('01.01.2010'))
        db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -100, viewcore.name_of_partner())

        abrechnungs_text = db.abrechnen(set_ergebnis='%Ergebnis%', verhaeltnis=70, set_other_kategorie='Ausgleich')

        assert len(db.einzelbuchungen.content) == 1

        uebertragene_buchung = db.einzelbuchungen.get(0)

        assert uebertragene_buchung['Name'] == 'some name'
        assert uebertragene_buchung['Datum'] == datum('17.03.2017')
        assert uebertragene_buchung['Kategorie'] == 'some kategorie'
        assert uebertragene_buchung['Wert'] == '-70.00'

        assert abrechnungs_text == self.abrechnung_verhaeltnis_other


    def test_abrechnen_shouldPrintFileContent(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.gemeinsamebuchungen.add(datum('17.03.2017'), 'some kategorie', 'some name', -10, viewcore.name_of_partner())
        time.stub_today_with(datum('01.01.2010'))
        abrechnungs_text = db.abrechnen(set_ergebnis="%Ergebnis%")
        time.reset_viewcore_stubs()

        assert abrechnungs_text == self.abrechnung

    def test_taint_shouldIncreaseTaintNumber(self):
        self.set_up()
        db = persisted_state.database_instance()

        assert db.taint_number() == 0
        db.taint()
        assert db.taint_number() == 1

    def test_isTainted_shouldReturnFalseWhenTainted(self):
        self.set_up()
        db = persisted_state.database_instance()

        assert not db.is_tainted()
        db.taint()
        assert db.is_tainted()

    def test_deTaint_shouldDeTaint(self):
        self.set_up()
        db = persisted_state.database_instance()

        db.taint()
        assert db.is_tainted()

        db.de_taint()
        assert not db.is_tainted()

    def test_deTaint_shouldDeTaintDauerauftraege(self):
        self.set_up()
        db = persisted_state.database_instance()

        db.dauerauftraege.taint()
        assert db.is_tainted()
        db.de_taint()
        assert not db.is_tainted()

    def test_tainNumber_shouldIncludeDauerauftraege(self):
        self.set_up()
        db = persisted_state.database_instance()

        assert db.taint_number() == 0
        db.dauerauftraege.taint()
        assert db.taint_number() == 1

    def test_deTaint_shouldDeTaintGemeinsameBuchungen(self):
        self.set_up()
        db = persisted_state.database_instance()

        db.gemeinsamebuchungen.taint()
        assert db.is_tainted()
        db.de_taint()
        assert not db.is_tainted()

    def test_deTaint_shouldDeTaintSparbuchungen(self):
        self.set_up()
        db = persisted_state.database_instance()

        db.sparbuchungen.taint()
        assert db.is_tainted()
        db.de_taint()
        assert not db.is_tainted()

    def test_taintNumber_shouldIncludeGemeinsameBuchungen(self):
        self.set_up()
        db = persisted_state.database_instance()

        assert db.taint_number() == 0
        db.gemeinsamebuchungen.taint()
        assert db.taint_number() == 1

    def test_taintNumber_shouldIncludeSparbuchungen(self):
        self.set_up()
        db = persisted_state.database_instance()

        assert db.taint_number() == 0
        db.sparbuchungen.taint()
        assert db.taint_number() == 1

    def test_deTaint_shouldDeTaintEinzelbuchungen(self):
        self.set_up()
        db = persisted_state.database_instance()

        db.einzelbuchungen.taint()
        assert db.is_tainted()
        db.de_taint()
        assert not db.is_tainted()

    def test_tainNumber_shouldIncludeEinzelbuchungen(self):
        self.set_up()
        db = persisted_state.database_instance()

        assert db.taint_number() == 0
        db.einzelbuchungen.taint()
        assert db.taint_number() == 1

    def test_deTaint_shouldDeTaintKontos(self):
        self.set_up()
        db = persisted_state.database_instance()

        db.sparkontos.taint()
        assert db.is_tainted()
        db.de_taint()
        assert not db.is_tainted()

    def test_tainNumber_shouldIncludeKontos(self):
        self.set_up()
        db = persisted_state.database_instance()

        assert db.taint_number() == 0
        db.sparkontos.taint()
        assert db.taint_number() == 1


    def test_deTaint_shouldDeTaintDepotwerte(self):
        self.set_up()
        db = persisted_state.database_instance()

        db.depotwerte.taint()
        assert db.is_tainted()
        db.de_taint()
        assert not db.is_tainted()

    def test_tainNumber_shouldIncludeDepotwerte(self):
        self.set_up()
        db = persisted_state.database_instance()

        assert db.taint_number() == 0
        db.depotwerte.taint()
        assert db.taint_number() == 1


    def test_deTaint_shouldDeTaintOrder(self):
        self.set_up()
        db = persisted_state.database_instance()

        db.order.taint()
        assert db.is_tainted()
        db.de_taint()
        assert not db.is_tainted()

    def test_tainNumber_shouldIncludeOrder(self):
        self.set_up()
        db = persisted_state.database_instance()

        assert db.taint_number() == 0
        db.order.taint()
        assert db.taint_number() == 1


    def test_deTaint_shouldDeTaintDepotauszuege(self):
        self.set_up()
        db = persisted_state.database_instance()

        db.depotauszuege.taint()
        assert db.is_tainted()
        db.de_taint()
        assert not db.is_tainted()

    def test_tainNumber_shouldIncludeDepotauszuege(self):
        self.set_up()
        db = persisted_state.database_instance()

        assert db.taint_number() == 0
        db.depotauszuege.taint()
        assert db.taint_number() == 1


class converter_test(unittest.TestCase):

    def test_frame_to_list_of_dicts_withEmptyDataframe_shouldReturnEmptyList(self):
        empty_dataframe = DataFrame()

        result = Database('test_database').frame_to_list_of_dicts(empty_dataframe)

        assert result == []

    def test_frame_to_list_of_dicts_withDataframe_shouldReturnListOfDicts(self):
        dataframe = DataFrame([{'col1': 'test1', 'col2': 1}, {'col1': 'test2', 'col2': 2}])

        result = Database('test_database').frame_to_list_of_dicts(dataframe)

        assert len(result) == 2
        assert result[0]['col1'] == 'test1'
        assert result[0]['col2'] == 1
        assert result[1]['col1'] == 'test2'
        assert result[1]['col2'] == 2


class Refresh(unittest.TestCase):

    def teste_refresh_with_empty_database(self):
        component_under_test = Database('test_database')
        component_under_test.refresh()

    def teste_refresh_shouldAddEinzelbuchungenVonDauerauftrag(self):
        component_under_test = Database('test_database')
        component_under_test.dauerauftraege.add(datum('10.01.2010'), datum('11.03.2010'), '', '', 'monatlich', 20)
        component_under_test.refresh()

        assert len(component_under_test.einzelbuchungen.content) == 3
