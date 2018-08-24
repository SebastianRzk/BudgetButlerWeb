'''
Created on 23.11.2017

@author: sebastian
'''
from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import enter_test_mode
from SeleniumTest import define_kategorie
from SeleniumTest import select_option
from SeleniumTest import get_selected_option
import time

class TestUI(SeleniumTestClass):
    def teste_ausgaben(self, get_driver, close_driver):
        self._generic_test(get_driver, close_driver, 'addausgabe', 'Neue Ausgabe')

    def teste_einnahmen(self, get_driver, close_driver):
        self._generic_test(get_driver, close_driver, 'addeinnahme', 'Neue Einnahme')

    def teste_dauerauftrag(self, get_driver, close_driver):
        self._generic_test(get_driver, close_driver, 'adddauerauftrag', 'Neuer Dauerauftrag')

    def teste_gemeinsam(self, get_driver, close_driver):
        self._generic_test(get_driver, close_driver, 'addgemeinsam', 'Neue gemeinsame Ausgabe')

    def _generic_test(self, get_driver, close_driver, pagename, pagetitle):
        driver = get_driver()
        enter_test_mode(driver)
        driver.get('http://localhost:5000/' + pagename + '/')

        verify_no_kategories_defined(driver)

        open_table_button = driver.find_element_by_id('open_add_kategorie')
        open_table_button.click()
        time.sleep(1)

        fill_element(driver, 'neue_kategorie', 'fancy test')

        add_kategorie_button = driver.find_element_by_id('add_kategorie')
        add_kategorie_button.click()
        time.sleep(1)

        verify_kategorie_defined(driver, 'fancy test')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == pagetitle
        close_driver(driver)

def verify_no_kategories_defined(driver):
    el = driver.find_element_by_id('kategorie_auswahl')

    assert len(el.find_elements_by_tag_name('option')) == 0

def verify_kategorie_defined(driver, kategorie):
    el = driver.find_element_by_id('kategorie_auswahl')
    for option in el.find_elements_by_tag_name('option'):
        assert option.text == kategorie
