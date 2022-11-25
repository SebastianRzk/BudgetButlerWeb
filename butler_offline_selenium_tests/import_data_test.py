from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import enter_test_mode
from butler_offline_selenium_tests.page.core.im_port import Import
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchungen_uebersicht import EinzelbuchungenUebersicht
from butler_offline_selenium_tests.page.core.configuration import Configuration


class TestUI(SeleniumTestClass):

    _data = '''
#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-06,Essen,Edeka,-10.0,True
#######MaschinenimportEnd
            '''

    def teste_import_neue_kategorien(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_import = Import(driver=driver)
        page_einzelbuchungen_uebersicht = EinzelbuchungenUebersicht(driver=driver)

        page_import.visit()
        page_import.import_data(data=self._data)

        assert page_import.page_name() == 'Kategorien zuweisen'

        page_import.click_action()

        page_einzelbuchungen_uebersicht.visit()
        page_einzelbuchungen_uebersicht.open_module(month=3, year=2017)

        assert page_einzelbuchungen_uebersicht.get_item_in_opened_module(0) == {
            'name': 'Edeka',
            'kategorie': 'Essen',
            'datum': '06.03.2017',
            'wert': '-10,00'
        }
        close_driver(driver)

    def test_with_mapping_to_other_kategorie(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_import = Import(driver=driver)
        page_einzelbuchungen_uebersicht = EinzelbuchungenUebersicht(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('nicht essen')

        page_import.visit()
        page_import.import_data(data=self._data)
        assert page_import.page_name() == 'Kategorien zuweisen'

        page_import.select_mapping('Essen', 'nicht essen')
        page_import.click_action()

        page_einzelbuchungen_uebersicht.visit()
        page_einzelbuchungen_uebersicht.open_module(month=3, year=2017)

        assert page_einzelbuchungen_uebersicht.get_item_in_opened_module(0) == {
            'name': 'Edeka',
            'kategorie': 'nicht essen',
            'datum': '06.03.2017',
            'wert': '-10,00'
        }
        close_driver(driver)


    def test_with_existing_kategorie(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_import = Import(driver=driver)
        page_einzelbuchungen_uebersicht = EinzelbuchungenUebersicht(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('Essen')

        page_import.visit()
        page_import.import_data(data=self._data)
        assert page_import.page_name() == 'Export / Import'

        page_einzelbuchungen_uebersicht.visit()
        page_einzelbuchungen_uebersicht.open_module(month=3, year=2017)

        assert page_einzelbuchungen_uebersicht.get_item_in_opened_module(0) == {
            'name': 'Edeka',
            'kategorie': 'Essen',
            'datum': '06.03.2017',
            'wert': '-10,00'
        }

        close_driver(driver)

    def test_should_showSuccessMessage(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_import = Import(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('Essen')

        page_import.visit()
        page_import.import_data(data=self._data)
        assert page_import.page_name() == 'Export / Import'

        assert page_import.get_message() == '1 Buchung wurde importiert'
        close_driver(driver)









