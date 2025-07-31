import logging

from butler_offline_selenium_tests.page.core.configuration import Configuration
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchungen_uebersicht import EinzelbuchungenUebersicht
from butler_offline_selenium_tests.page.gemeinsam.gemeinsam_abrechnen import GemeinsamAbrechnen
from butler_offline_selenium_tests.page.gemeinsam.gemeinsam_add import GemeinsamAdd, DEFAULT_PARTNERNAME
from butler_offline_selenium_tests.page.util import enter_test_mode, define_kategorie
from butler_offline_selenium_tests.selenium_test import SeleniumTestClass


class TestGemeinsameAbrechnung(SeleniumTestClass):
    test_change_veraeltnis_abrechnung = '''mock titel
Abrechnung vom 22.01.2019 (von 01.01.2010 bis einschließlich 01.01.2010
########################################


Ergebnis:
In dieser Abrechnung wurden 1 Buchungen im Zeitraum von 01.01.2010 bis 01.01.2010 betrachtet, welche einen Gesamtbetrag von -100,00€ umfassen.
Es wurde angenommen, dass diese in einem Verhältnis von 70% (Test_User) zu 30% (kein_Partnername_gesetzt) aufgeteilt werden sollen.
Es wurde kein Limit für die Abrechnung definiert.
Um die Differenz auszugleichen, sollte Test_User 70,00€ an kein_Partnername_gesetzt überweisen.


Erfasste Ausgaben:

kein_Partnername_gesetzt -100,00€
Test_User          0,00€
----------------------
Gesamt          -100,00€


########################################
Ausgaben von kein_Partnername_gesetzt
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2010   0name           0test_kategorie            -100,00€


########################################
Ausgaben von Test_User
########################################
Datum        Name            Kategorie                   Betrag€



#######MaschinenimportMetadatenStart
Abrechnungsdatum:2019-01-22
Abrechnende Person:kein_Partnername_gesetzt
Titel:mock titel
Ziel:GemeinsameAbrechnungFuerPartner
Ausfuehrungsdatum:2019-01-22
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2010-01-01,0test_kategorie,0name,-50.00
2019-01-22,Unbekannt,mock titel,20.00
#######MaschinenimportEnd'''

    def test_change_verhaeltnis(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_gemeinsam_abrechnen = GemeinsamAbrechnen(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2010-01-01', '0name', '0test_kategorie', '100', DEFAULT_PARTNERNAME)

        page_gemeinsam_abrechnen.visit()

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0,00',
            'ausgabe_self_soll': '-50,00',
            'ausgabe_self_diff': '-50,00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '-100,00',
            'ausgabe_partner_soll': '-50,00',
            'ausgabe_partner_diff': '50,00'
        }

        page_gemeinsam_abrechnen.update_abrechnungsverhältnis(70)

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0,00',
            'ausgabe_self_soll': '-70,00',
            'ausgabe_self_diff': '-70,00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '-100,00',
            'ausgabe_partner_soll': '-30,00',
            'ausgabe_partner_diff': '70,00'
        }

        page_gemeinsam_abrechnen.abrechnen()

        logging.info(str(page_gemeinsam_abrechnen.abrechnung_partner_result()))
        assert page_gemeinsam_abrechnen.abrechnung_partner_result() == self.test_change_veraeltnis_abrechnung
        close_driver(driver)

    set_limit_abrechnung = '''mock titel
Abrechnung vom 22.01.2019 (von 01.01.2010 bis einschließlich 01.01.2010
########################################


Ergebnis:
In dieser Abrechnung wurden 1 Buchungen im Zeitraum von 01.01.2010 bis 01.01.2010 betrachtet, welche einen Gesamtbetrag von -100,00€ umfassen.
Es wurde angenommen, dass diese in einem Verhältnis von 50% (Test_User) zu 50% (kein_Partnername_gesetzt) aufgeteilt werden sollen.
Für die Abrechnung wurde ein Limit von -30,00€ für Test_User definiert
Das Limit wurde überschritten. Das neue Verhältnis ist wie folgt:.
Test_User: 30,00% (-30,00€) , kein_Partnername_gesetzt: 70,00% (-70,00€)
Um die Differenz auszugleichen, sollte Test_User 30,00€ an kein_Partnername_gesetzt überweisen.


Erfasste Ausgaben:

kein_Partnername_gesetzt -100,00€
Test_User          0,00€
----------------------
Gesamt          -100,00€


########################################
Ausgaben von kein_Partnername_gesetzt
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2010   0name           0test_kategorie            -100,00€


########################################
Ausgaben von Test_User
########################################
Datum        Name            Kategorie                   Betrag€



#######MaschinenimportMetadatenStart
Abrechnungsdatum:2019-01-22
Abrechnende Person:kein_Partnername_gesetzt
Titel:mock titel
Ziel:GemeinsameAbrechnungFuerPartner
Ausfuehrungsdatum:2019-01-22
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2010-01-01,0test_kategorie,0name,-50.00
2019-01-22,Unbekannt,mock titel,-20.00
#######MaschinenimportEnd'''

    def test_set_limit(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_gemeinsam_abrechnen = GemeinsamAbrechnen(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2010-01-01', '0name', '0test_kategorie', '100', DEFAULT_PARTNERNAME)

        page_gemeinsam_abrechnen.visit()

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0,00',
            'ausgabe_self_soll': '-50,00',
            'ausgabe_self_diff': '-50,00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '-100,00',
            'ausgabe_partner_soll': '-50,00',
            'ausgabe_partner_diff': '50,00'
        }

        page_gemeinsam_abrechnen.update_limit(person='Test_User', value=30)

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0,00',
            'ausgabe_self_soll': '-30,00',
            'ausgabe_self_diff': '-30,00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '-100,00',
            'ausgabe_partner_soll': '-70,00',
            'ausgabe_partner_diff': '30,00'
        }

        page_gemeinsam_abrechnen.abrechnen()

        logging.info(str(page_gemeinsam_abrechnen.abrechnung_partner_result()))
        assert page_gemeinsam_abrechnen.abrechnung_partner_result() == self.set_limit_abrechnung
        close_driver(driver)

    set_limit_abrechnung_ausgleich = '''mock titel
Abrechnung vom 22.01.2019 (von 01.01.2010 bis einschließlich 01.01.2010
########################################


Ergebnis:
In dieser Abrechnung wurden 1 Buchungen im Zeitraum von 01.01.2010 bis 01.01.2010 betrachtet, welche einen Gesamtbetrag von -100,00€ umfassen.
Es wurde angenommen, dass diese in einem Verhältnis von 50% (Test_User) zu 50% (kein_Partnername_gesetzt) aufgeteilt werden sollen.
Für die Abrechnung wurde ein Limit von -30,00€ für Test_User definiert
Das Limit wurde überschritten. Das neue Verhältnis ist wie folgt:.
Test_User: 30,00% (-30,00€) , kein_Partnername_gesetzt: 70,00% (-70,00€)
Um die Differenz auszugleichen, sollte Test_User 30,00€ an kein_Partnername_gesetzt überweisen.


Erfasste Ausgaben:

kein_Partnername_gesetzt -100,00€
Test_User          0,00€
----------------------
Gesamt          -100,00€


########################################
Ausgaben von kein_Partnername_gesetzt
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2010   0name           0test_kategorie            -100,00€


########################################
Ausgaben von Test_User
########################################
Datum        Name            Kategorie                   Betrag€



#######MaschinenimportMetadatenStart
Abrechnungsdatum:2019-01-22
Abrechnende Person:kein_Partnername_gesetzt
Titel:mock titel
Ziel:GemeinsameAbrechnungFuerPartner
Ausfuehrungsdatum:2019-01-22
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2010-01-01,0test_kategorie,0name,-50.00
2019-01-22,test ausgleich,mock titel,-20.00
#######MaschinenimportEnd'''

    def test_set_limit_and_add_ausgleichsbuchungen_both(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')

        page_configuration = Configuration(driver=driver)
        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_gemeinsam_abrechnen = GemeinsamAbrechnen(driver=driver)
        page_einzelbuchung_uebersicht = EinzelbuchungenUebersicht(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2010-01-01', '0name', '0test_kategorie', '100', DEFAULT_PARTNERNAME)

        page_configuration.visit()
        page_configuration.define_kategorie('1test_kategorie')

        page_gemeinsam_abrechnen.visit()

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0,00',
            'ausgabe_self_soll': '-50,00',
            'ausgabe_self_diff': '-50,00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '-100,00',
            'ausgabe_partner_soll': '-50,00',
            'ausgabe_partner_diff': '50,00'
        }

        page_gemeinsam_abrechnen.update_limit('Test_User', 30)
        page_gemeinsam_abrechnen.set_self_kategorie('1test_kategorie')
        page_gemeinsam_abrechnen.set_other_kategorie('test ausgleich')

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0,00',
            'ausgabe_self_soll': '-30,00',
            'ausgabe_self_diff': '-30,00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '-100,00',
            'ausgabe_partner_soll': '-70,00',
            'ausgabe_partner_diff': '30,00'
        }

        page_gemeinsam_abrechnen.abrechnen()

        assert page_gemeinsam_abrechnen.abrechnung_partner_result() == self.set_limit_abrechnung_ausgleich

        page_einzelbuchung_uebersicht.visit()
        page_einzelbuchung_uebersicht.open_module(month=1, year=2019)

        assert page_einzelbuchung_uebersicht.get_item_in_opened_module(2) == {
            'name': 'mock titel',
            'kategorie': '1test_kategorie',
            'datum': '22.01.2019',
            'wert': '20,00 €'
        }

        page_einzelbuchung_uebersicht.open_year(year=2010)
        page_einzelbuchung_uebersicht.open_module(month=1, year=2010)

        assert page_einzelbuchung_uebersicht.get_item_in_opened_module(1) == {
            'name': '0name',
            'kategorie': '0test_kategorie',
            'datum': '01.01.2010',
            'wert': '-50,00 €'
        }

        close_driver(driver)
