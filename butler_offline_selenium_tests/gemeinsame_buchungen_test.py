from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import enter_test_mode, define_kategorie, get_selected_option
from butler_offline_selenium_tests.page.gemeinsam.gemeinsam_add import GemeinsamAdd
from butler_offline_selenium_tests.page.gemeinsam.gemeinsam_uebersicht import GemeinsamUeberischt
from butler_offline_selenium_tests.page.core.configuration import Configuration


class TestUI(SeleniumTestClass):

    def teste_uebersicht(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_configuration = Configuration(driver=driver)
        page_gemeinsam_uebersicht = GemeinsamUeberischt(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2010-01-01', '0name', '0test_kategorie', '0.5', 'Partner')

        page_configuration.visit()
        page_configuration.define_kategorie('1test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2011-01-01', '1name', '1test_kategorie', 1, 'test')

        page_configuration.visit()
        page_configuration.define_kategorie('2test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2012-01-01', '2name', '2test_kategorie', 2, 'test')
        page_gemeinsam_add.add('2013-01-01', '3name', '1test_kategorie', 3, 'Partner')

        page_gemeinsam_uebersicht.visit()

        assert page_gemeinsam_uebersicht.get_row(2) == {
            'name': '2name',
            'kategorie': '2test_kategorie',
            'datum': '01.01.2012',
            'wert': '-2,00',
            'person': 'test'
        }
        close_driver(driver)

    def teste_vorbelegung_with_self(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_configuration = Configuration(driver=driver)
        page_gemeinsam_uebersicht = GemeinsamUeberischt(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2010-01-01', '0name', '0test_kategorie', '0.5', 'Partner')

        page_configuration.visit()
        page_configuration.define_kategorie('1test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2011-01-01', '1name', '1test_kategorie', 1, 'test')

        page_configuration.visit()
        page_configuration.define_kategorie('2test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2012-01-01', '2name', '2test_kategorie', 2, 'test')
        page_gemeinsam_add.add('2013-01-01', '3name', '1test_kategorie', 3, 'Partner')

        page_gemeinsam_uebersicht.visit()

        page_gemeinsam_uebersicht.click_edit_button(2)

        assert page_gemeinsam_add.get_vorbelegung() == {
            'name': '2name',
            'kategorie': '2test_kategorie',
            'person': 'test',
            'datum': '2012-01-01',
            'wert': '2,00'
        }
        close_driver(driver)

    def teste_vorbelegung_with_other(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)


        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_configuration = Configuration(driver=driver)
        page_gemeinsam_uebersicht = GemeinsamUeberischt(driver=driver)

        page_configuration.visit()
        page_configuration.define_kategorie('0test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2010-01-01', '0name', '0test_kategorie', '0.5', 'Partner')

        page_configuration.visit()
        page_configuration.define_kategorie('1test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2011-01-01', '1name', '1test_kategorie', 1, 'test')

        page_configuration.visit()
        page_configuration.define_kategorie('2test_kategorie')

        page_gemeinsam_add.visit()
        page_gemeinsam_add.add('2012-01-01', '2name', '2test_kategorie', 2, 'test')
        page_gemeinsam_add.add('2013-01-01', '3name', '1test_kategorie', 3, 'Partner')

        page_gemeinsam_uebersicht.visit()

        page_gemeinsam_uebersicht.click_edit_button(0)

        assert page_gemeinsam_add.get_vorbelegung() == {
            'name': '0name',
            'kategorie': '0test_kategorie',
            'person': 'Partner',
            'datum': '2010-01-01',
            'wert': '0,50'
        }
        close_driver(driver)



