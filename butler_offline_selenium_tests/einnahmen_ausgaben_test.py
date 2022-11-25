from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import enter_test_mode
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchung_add import EinzelbuchungAdd
from butler_offline_selenium_tests.page.core.configuration import Configuration
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchungen_uebersicht import EinzelbuchungenUebersicht


class TestUI(SeleniumTestClass):


    def teste_edit_vorbelegung(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_einzelbuchungen_add = EinzelbuchungAdd(driver=driver)
        page_einzelbuchungen_uebersicht = EinzelbuchungenUebersicht(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_einzelbuchungen_add.visit()
        page_einzelbuchungen_add.add('2010-01-01', '0name', '0test_kategorie', '0.5')

        page_configuration.visit()
        page_configuration.define_kategorie('1test_kategorie')

        page_einzelbuchungen_add.visit()
        page_einzelbuchungen_add.add('2011-01-01', '1name', '1test_kategorie', 1)

        page_configuration.visit()
        page_configuration.define_kategorie('2test_kategorie')

        page_einzelbuchungen_add.visit()
        page_einzelbuchungen_add.add('2012-01-01', '2name', '2test_kategorie', 2)
        page_einzelbuchungen_add.add('2012-12-01', '3name', '1test_kategorie', 3)


        page_einzelbuchungen_uebersicht.visit()
        page_einzelbuchungen_uebersicht.open_module(month=1, year=2012)

        assert page_einzelbuchungen_uebersicht.get_item_in_opened_module(2) == {
            'name': '2name',
            'kategorie': '2test_kategorie',
            'datum': '01.01.2012',
            'wert': '-2,00'
        }

        page_einzelbuchungen_uebersicht.click_edit_button(2)

        assert page_einzelbuchungen_add.get_vorbelegung() == {
            'name': '2name',
            'kategorie': '2test_kategorie',
            'datum': '2012-01-01',
            'wert': '2,00'
        }

        close_driver(driver)

