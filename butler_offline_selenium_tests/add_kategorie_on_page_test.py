from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import enter_test_mode, fill_element
from selenium.webdriver.common.by import By
import time

class TestUI(SeleniumTestClass):
    def teste_ausgaben(self, get_driver, close_driver):
        self._generic_test(get_driver, close_driver, 'addausgabe', 'Ausgabe hinzufügen')

    def teste_einnahmen(self, get_driver, close_driver):
        self._generic_test(get_driver, close_driver, 'addeinnahme', 'Einnahme hinzufügen')

    def teste_dauerauftrag(self, get_driver, close_driver):
        self._generic_test(get_driver, close_driver, 'adddauerauftrag', 'Dauerauftrag hinzufügen')

    def teste_gemeinsam(self, get_driver, close_driver):
        self._generic_test(get_driver, close_driver, 'addgemeinsam', 'Gemeinsame Buchung hinzufügen')

    def _generic_test(self, get_driver, close_driver, pagename, pagetitle):
        driver = get_driver()
        enter_test_mode(driver)
        driver.get('http://localhost:5000/' + pagename + '/')

        verify_no_kategories_defined(driver)

        open_table_button = driver.find_element(By.ID, 'open_add_kategorie')
        open_table_button.click()
        time.sleep(0.1)

        fill_element(driver, 'neue_kategorie', 'fancy test')

        add_kategorie_button = driver.find_element(By.ID, 'add_kategorie')
        add_kategorie_button.click()
        time.sleep(0.1)

        verify_kategorie_defined(driver, 'fancy test')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == pagetitle
        close_driver(driver)


def verify_no_kategories_defined(driver):
    el = driver.find_element(By.ID, 'kategorie_auswahl')

    assert len(el.find_elements(By.TAG_NAME, 'option')) == 0


def verify_kategorie_defined(driver, kategorie):
    el = driver.find_element(By.ID, 'kategorie_auswahl')
    for option in el.find_elements(By.TAG_NAME, 'option'):
        assert option.text == kategorie
