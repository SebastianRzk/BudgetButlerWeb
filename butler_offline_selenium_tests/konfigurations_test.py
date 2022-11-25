from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import enter_test_mode
from butler_offline_selenium_tests.page.gemeinsam.gemeinsam_add import GemeinsamAdd
from butler_offline_selenium_tests.page.core.configuration import Configuration
from butler_offline_selenium_tests.page.core.menu import Menu
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchung_add import EinzelbuchungAdd


class TestUI(SeleniumTestClass):

    def teste_change_partnername(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_configuration = Configuration(driver=driver)

        page_gemeinsam_add.visit()
        assert page_gemeinsam_add.partner_options() == set(['test', 'Partner'])

        page_configuration.visit()
        page_configuration.update_partnername('Olaf')

        page_gemeinsam_add.visit()
        assert page_gemeinsam_add.partner_options() == set(['test', 'Olaf'])
        close_driver(driver)

    def test_change_database(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_menu = Menu(driver=driver)

        page_gemeinsam_add.visit()
        assert page_gemeinsam_add.partner_options() == set(['test', 'Partner'])

        page_menu.change_database('test')
        assert page_menu.get_title() == '~~~test~~~'

        page_menu.change_database('Partner')
        assert page_menu.get_title() == '~~~Partner~~~'
        close_driver(driver)

    def teste_theme_color(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_einzelbuchungen_add = EinzelbuchungAdd(driver=driver)
        page_configuration = Configuration(driver=driver)

        page_einzelbuchungen_add.visit()
        assert page_einzelbuchungen_add.add_button_color() == 'rgb(0, 172, 214)'

        page_configuration.visit()
        page_configuration.update_theme_color('#000000')

        page_einzelbuchungen_add.visit()
        assert page_einzelbuchungen_add.add_button_color() == 'rgb(0, 0, 0)'

        close_driver(driver)

