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
    def teste_ausgaben(self, driver_provider):
        self._generic_test(driver_provider, 'addeinzelbuchung', 'Neue Ausgabe')

    def teste_einnahmen(self, driver_provider):
        self._generic_test(driver_provider, 'addeinnahme', 'Neue Einnahme')

    def teste_dauerauftrag(self, driver_provider):
        self._generic_test(driver_provider, 'adddauerauftrag', 'Neuer Dauerauftrag')

    def teste_gemeinsam(self, driver_provider):
        self._generic_test(driver_provider, 'addgemeinsam', 'Neue gemeinsame Ausgabe')

    def _generic_test(self, driver_provider, pagename, pagetitle):
        driver = driver_provider()
        enter_test_mode(driver)
        driver.get('http://localhost:8000/' + pagename + '/')

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
        driver.close()

def verify_no_kategories_defined(driver):
    el = driver.find_element_by_id('kategorie_auswahl')

    assert len(el.find_elements_by_tag_name('option')) == 0

def verify_kategorie_defined(driver, kategorie):
    el = driver.find_element_by_id('kategorie_auswahl')
    for option in el.find_elements_by_tag_name('option'):
        assert option.text == kategorie
