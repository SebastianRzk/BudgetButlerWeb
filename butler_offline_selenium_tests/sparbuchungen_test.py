from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import enter_test_mode
from butler_offline_selenium_tests.page.sparen.depot_add import DepotAdd
from butler_offline_selenium_tests.page.sparen.depot_uebersicht import DepotUebersicht
from butler_offline_selenium_tests.page.sparen.sparbuchung_add import SparbuchungAdd
from butler_offline_selenium_tests.page.sparen.sparbuchung_uebersicht import SparbuchungUebersicht
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchungen_uebersicht import EinzelbuchungenUebersicht


class TestUI(SeleniumTestClass):

    def teste_uebersicht_kontos(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_sparkonto_add = DepotAdd(driver=driver)
        page_sparbuchung_add = SparbuchungAdd(driver=driver)
        page_sparkonto_uebersicht = DepotUebersicht(driver=driver)

        page_sparkonto_add.visit()
        page_sparkonto_add.add('TestKonto', 'Sparkonto')

        page_sparbuchung_add.visit()
        page_sparbuchung_add.add('2020-01-01', 'testname', 'Manueller Auftrag', 'TestKonto', 10,  True)

        page_sparkonto_uebersicht.visit()

        assert page_sparkonto_uebersicht.get(0) == {
            'name': 'TestKonto',
            'typ': 'Sparkonto',
            'wert': '10,00',
            'aufbuchungen': '10,00',
            'difference': '0,00'
        }

        assert page_sparkonto_uebersicht.get_gesamt() == {
            'wert': '10,00',
            'aufbuchungen': '10,00',
            'difference': '0,00'
        }
        close_driver(driver)

    def teste_uebersicht_sparbuchungen(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_sparkonto_add = DepotAdd(driver=driver)
        page_sparbuchung_add = SparbuchungAdd(driver=driver)
        page_sparbuchungen_uebersicht = SparbuchungUebersicht(driver=driver)
        page_einzelbuchung_uebersicht = EinzelbuchungenUebersicht(driver=driver)

        page_sparkonto_add.visit()
        page_sparkonto_add.add('TestKonto', 'Sparkonto')
        page_sparbuchung_add.visit()
        page_sparbuchung_add.add('2020-01-01', 'testname', 'Manueller Auftrag', 'TestKonto', 10,  True)

        page_sparbuchungen_uebersicht.visit()
        driver.get('http://localhost:5000/uebersicht_sparbuchungen/')

        page_sparbuchungen_uebersicht.open_module(month=1, year=2020)

        assert page_sparbuchungen_uebersicht.get(0) == {
            'name': 'testname',
            'konto': 'TestKonto',
            'typ': 'Manueller Auftrag',
            'wert': '10,00'
        }

        page_einzelbuchung_uebersicht.visit()
        page_einzelbuchung_uebersicht.open_module(month=1, year=2020)

        assert page_einzelbuchung_uebersicht.get_item_in_opened_module(0) == {
            'name': 'testname',
            'datum': '01.01.2020',
            'kategorie': 'Sparen',
            'wert': '-10,00'
        }
        close_driver(driver)

