from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import content_of, enter_test_mode, define_kategorie
import logging
from butler_offline_selenium_tests.page.core.configuration import Configuration
from butler_offline_selenium_tests.page.gemeinsam.gemeinsam_add import GemeinsamAdd
from butler_offline_selenium_tests.page.gemeinsam.gemeinsam_abrechnen import GemeinsamAbrechnen
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchungen_uebersicht import EinzelbuchungenUebersicht

class TestGemeinsameAbrechnung(SeleniumTestClass):
    test_change_veraeltnis_abrechnung = '''
			Abrechnung vom 22.01.2019 (01.01.2010-01.01.2010)
########################################
 Ergebnis:
test übernimmt einen Anteil von 70% der Ausgaben.

Partner bekommt von test noch 70.00€.

Ausgaben von Partner          -100.00
Ausgaben von test                0.00
--------------------------------------
Gesamt                        -100.00


########################################
 Ausgaben von Partner
########################################
 Datum      Kategorie    Name                    Wert
01.01.2010  0test_kategorie 0name                -100.00


########################################
 Ausgaben von test
########################################
 Datum      Kategorie    Name                    Wert


#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2010-01-01,0test_kategorie,0name,-30.00,False
#######MaschinenimportEnd

		'''

    def test_change_verhaeltnis(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_gemeinsam_abrechnen = GemeinsamAbrechnen(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2010-01-01', '0name', '0test_kategorie', '100', 'Partner')

        page_gemeinsam_abrechnen.visit()

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0.00',
            'ausgabe_self_soll': '50.00',
            'ausgabe_self_diff': '-50.00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '100.00',
            'ausgabe_partner_soll': '50.00',
            'ausgabe_partner_diff': '50.00'
        }

        page_gemeinsam_abrechnen.update_abrechnungsverhältnis(70)

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0.00',
            'ausgabe_self_soll': '70.00',
            'ausgabe_self_diff': '-70.00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '100.00',
            'ausgabe_partner_soll': '30.00',
            'ausgabe_partner_diff': '70.00'
        }

        page_gemeinsam_abrechnen.abrechnen()

        logging.info(str(page_gemeinsam_abrechnen.abrechnung_result()))
        assert page_gemeinsam_abrechnen.abrechnung_result() == self.test_change_veraeltnis_abrechnung
        close_driver(driver)

    set_limit_abrechnung = '''
			Abrechnung vom 22.01.2019 (01.01.2010-01.01.2010)
########################################
 Ergebnis:
Durch das Limit bei test von 30 EUR wurde das Verhältnis von 50 auf 30.0 aktualisiert

Partner bekommt von test noch 30.00€.

Ausgaben von Partner          -100.00
Ausgaben von test                0.00
--------------------------------------
Gesamt                        -100.00


########################################
 Ausgaben von Partner
########################################
 Datum      Kategorie    Name                    Wert
01.01.2010  0test_kategorie 0name                -100.00


########################################
 Ausgaben von test
########################################
 Datum      Kategorie    Name                    Wert


#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2010-01-01,0test_kategorie,0name,-70.00,False
#######MaschinenimportEnd

		'''

    def test_set_limit(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_gemeinsam_abrechnen = GemeinsamAbrechnen(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2010-01-01', '0name', '0test_kategorie', '100', 'Partner')

        page_gemeinsam_abrechnen.visit()

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0.00',
            'ausgabe_self_soll': '50.00',
            'ausgabe_self_diff': '-50.00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '100.00',
            'ausgabe_partner_soll': '50.00',
            'ausgabe_partner_diff': '50.00'
        }

        page_gemeinsam_abrechnen.update_limit(person='test', value=30)


        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0.00',
            'ausgabe_self_soll': '30.00',
            'ausgabe_self_diff': '-30.00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '100.00',
            'ausgabe_partner_soll': '70.00',
            'ausgabe_partner_diff': '30.00'
        }

        page_gemeinsam_abrechnen.abrechnen()

        logging.info(str(page_gemeinsam_abrechnen.abrechnung_result()))
        assert page_gemeinsam_abrechnen.abrechnung_result() == self.set_limit_abrechnung
        close_driver(driver)

    set_limit_abrechnung_ausgleich = '''
			Abrechnung vom 22.01.2019 (01.01.2010-01.01.2010)
########################################
 Ergebnis:
Durch das Limit bei test von 30 EUR wurde das Verhältnis von 50 auf 30.0 aktualisiert

Partner bekommt von test noch 30.00€.

Ausgaben von Partner          -100.00
Ausgaben von test                0.00
--------------------------------------
Gesamt                        -100.00


########################################
 Ausgaben von Partner
########################################
 Datum      Kategorie    Name                    Wert
01.01.2010  0test_kategorie 0name                -100.00


########################################
 Ausgaben von test
########################################
 Datum      Kategorie    Name                    Wert


#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2010-01-01,0test_kategorie,0name,-50.00,False
2010-01-01,test ausgleich,test ausgleich,-20.00,False
#######MaschinenimportEnd

		'''

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
        page_gemeinsam_add.add('2010-01-01', '0name', '0test_kategorie', '100', 'Partner')

        page_configuration.visit()
        page_configuration.define_kategorie('1test_kategorie')

        page_gemeinsam_abrechnen.visit()

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0.00',
            'ausgabe_self_soll': '50.00',
            'ausgabe_self_diff': '-50.00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '100.00',
            'ausgabe_partner_soll': '50.00',
            'ausgabe_partner_diff': '50.00'
        }

        page_gemeinsam_abrechnen.update_limit('test', 30)
        page_gemeinsam_abrechnen.set_self_kategorie('1test_kategorie')
        page_gemeinsam_abrechnen.set_other_kategorie('test ausgleich')

        assert page_gemeinsam_abrechnen.result_self() == {
            'ausgabe_self': '0.00',
            'ausgabe_self_soll': '30.00',
            'ausgabe_self_diff': '-30.00'
        }

        assert page_gemeinsam_abrechnen.result_partner() == {
            'ausgabe_partner': '100.00',
            'ausgabe_partner_soll': '70.00',
            'ausgabe_partner_diff': '30.00'
        }

        page_gemeinsam_abrechnen.abrechnen()

        assert page_gemeinsam_abrechnen.abrechnung_result() == self.set_limit_abrechnung_ausgleich

        page_einzelbuchung_uebersicht.visit()
        page_einzelbuchung_uebersicht.open_module(month=1, year=2010)

        assert page_einzelbuchung_uebersicht.get_item_in_opened_module(0) == {
            'name': '0name',
            'kategorie': '0test_kategorie',
            'datum': '01.01.2010',
            'wert': '-50,00'
        }

        assert page_einzelbuchung_uebersicht.get_item_in_opened_module(1) == {
            'name': '1test_kategorie',
            'kategorie': '1test_kategorie',
            'datum': '01.01.2010',
            'wert': '20,00'
        }

        close_driver(driver)


