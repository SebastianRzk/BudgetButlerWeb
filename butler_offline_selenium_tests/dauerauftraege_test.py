from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import enter_test_mode
from butler_offline_selenium_tests.page.einzelbuchungen.dauerauftrag_add import DauerauftragAdd
from butler_offline_selenium_tests.page.core.configuration import Configuration
from butler_offline_selenium_tests.page.einzelbuchungen.dauerautrag_uebersicht import DauerauftragUebersicht
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchungen_uebersicht import EinzelbuchungenUebersicht


class TestUI(SeleniumTestClass):

    def teste_uebersicht(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_dauerauftrag_add = DauerauftragAdd(driver=driver)
        page_dauerauftrag_uebersicht = DauerauftragUebersicht(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add('2010-01-01', '2010-02-02', '0name', '0test_kategorie', '0.5', 'Einnahme')

        page_configuration.visit()
        page_configuration.define_kategorie('1test_kategorie')

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add('2011-01-01', '2011-02-02', '1name', '1test_kategorie', 1, 'Ausgabe')

        page_configuration.visit()
        page_configuration.define_kategorie('2test_kategorie')

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add('2012-01-01', '2012-02-02', '2name', '2test_kategorie', 2, 'Ausgabe')
        page_dauerauftrag_add.add('2013-01-01', '2013-02-02', '3name', '1test_kategorie', 3, 'Einnahme')

        page_dauerauftrag_uebersicht.visit()
        assert page_dauerauftrag_uebersicht.get_row(id=2) == {
            'id': '2',
            'name': '2name',
            'kategorie': '2test_kategorie',
            'startdatum': '01.01.2012',
            'endedatum': '02.02.2012',
            'wert': '-2.00'
        }
        close_driver(driver)

    def teste_edit_vorbelegung_ausgabe(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_dauerauftrag_add = DauerauftragAdd(driver=driver)
        page_dauerauftrag_uebersicht = DauerauftragUebersicht(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add('2010-01-01', '2010-02-02', '0name', '0test_kategorie', '0.5', 'Einnahme')

        page_configuration.visit()
        page_configuration.define_kategorie('1test_kategorie')

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add('2011-01-01', '2011-02-02', '1name', '1test_kategorie', 1, 'Ausgabe')

        page_configuration.visit()
        page_configuration.define_kategorie('2test_kategorie')

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add('2012-01-01', '2012-02-02', '2name', '2test_kategorie', 2, 'Ausgabe', rhythmus='jaehrlich')
        page_dauerauftrag_add.add('2013-01-01', '2013-02-02', '3name', '1test_kategorie', 3, 'Einnahme')

        page_dauerauftrag_uebersicht.visit()

        page_dauerauftrag_uebersicht.click_edit_button(2)

        assert page_dauerauftrag_add.get_vorbelegung() == {
            'name': '2name',
            'kategorie': '2test_kategorie',
            'typ': 'Ausgabe',
            'rhythmus': 'jaehrlich',
            'startdatum': '2012-01-01',
            'endedatum': '2012-02-02',
            'wert': '2,00'
        }

        close_driver(driver)

    def teste_edit_vorbelegung_einnahme(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_dauerauftrag_add = DauerauftragAdd(driver=driver)
        page_dauerauftrag_uebersicht = DauerauftragUebersicht(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add('2010-01-01', '2010-02-02', '0name', '0test_kategorie', '0.5', 'Einnahme')

        page_configuration.visit()
        page_configuration.define_kategorie('1test_kategorie')

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add('2011-01-01', '2011-02-02', '1name', '1test_kategorie', 1, 'Ausgabe')

        page_configuration.visit()
        page_configuration.define_kategorie('2test_kategorie')

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add('2012-01-01', '2012-02-02', '2name', '2test_kategorie', 2, 'Ausgabe', rhythmus='jaehrlich')
        page_dauerauftrag_add.add('2013-01-01', '2013-02-02', '3name', '1test_kategorie', 3, 'Einnahme')

        page_dauerauftrag_uebersicht.visit()

        page_dauerauftrag_uebersicht.click_edit_button(0)

        assert page_dauerauftrag_add.get_vorbelegung() == {
            'name': '0name',
            'kategorie': '0test_kategorie',
            'typ': 'Einnahme',
            'rhythmus': 'monatlich',
            'startdatum': '2010-01-01',
            'endedatum': '2010-02-02',
            'wert': '0,50'
        }

        close_driver(driver)

    def teste_vierteljaehrlich(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_dauerauftrag_add = DauerauftragAdd(driver=driver)
        page_einzelbuchungen = EinzelbuchungenUebersicht(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('2test_kategorie')

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add('2010-01-31', '2010-08-02', '2name', '2test_kategorie', 2, 'Ausgabe', rhythmus='vierteljaehrlich')

        page_einzelbuchungen.visit()

        page_einzelbuchungen.open_module(year=2010, month=1)

        assert page_einzelbuchungen.get_item_in_opened_module(0) == {
            'name': '2name',
            'kategorie': '2test_kategorie',
            'datum': '31.01.2010',
            'wert': '-2,00'
        }

        page_einzelbuchungen.open_module(year=2010, month=4)

        assert page_einzelbuchungen.get_item_in_opened_module(1) == {
            'name': '2name',
            'kategorie': '2test_kategorie',
            'datum': '30.04.2010',
            'wert': '-2,00'
        }
        page_einzelbuchungen.open_module(year=2010, month=7)

        assert page_einzelbuchungen.get_item_in_opened_module(2) == {
            'name': '2name',
            'kategorie': '2test_kategorie',
            'datum': '31.07.2010',
            'wert': '-2,00'
        }

        close_driver(driver)

