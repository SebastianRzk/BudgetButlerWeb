'''
Created on 23.11.2017

@author: sebastian
'''
from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import enter_test_mode
from SeleniumTest import define_kategorie
from SeleniumTest import select_option
from time import sleep
from SeleniumTest import get_selected_option

class TestUI(SeleniumTestClass):
    def _add_ausgabe(self, driver, date, name, kategorie, wert, person):
        driver.get('http://localhost:8000/addgemeinsam/')
        fill_element(driver, 'date', date)
        fill_element(driver, 'name', name)
        fill_element(driver, 'wert', wert)
        select_option(driver, 'kategorie_auswahl', kategorie)
        select_option(driver, 'person_auswahl', person)


        add_button = driver.find_element_by_id('add')
        add_button.click()

        base_table = driver.find_element_by_id('letzte_erfassungen')
        tableRows = base_table.find_elements_by_tag_name('tr')

    def teste_uebersicht(self, driver_provider):
        driver = driver_provider()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_ausgabe(driver, '01012010', '0name', '0test_kategorie', '0.5', 'Maureen')
        define_kategorie(driver, '1test_kategorie')
        self._add_ausgabe(driver, '01012011', '1name', '1test_kategorie', 1, 'test')
        define_kategorie(driver, '2test_kategorie')
        self._add_ausgabe(driver, '01012012', '2name', '2test_kategorie', 2, 'test')
        self._add_ausgabe(driver, '01012013', '3name', '1test_kategorie', 3, 'Maureen')

        driver.get('http://localhost:8000/gemeinsameuebersicht/')

        assert driver.find_element_by_id('item_2_id').get_attribute('innerHTML') == '2'
        assert driver.find_element_by_id('item_2_name').get_attribute('innerHTML') == '2name'
        assert driver.find_element_by_id('item_2_kategorie').get_attribute('innerHTML') == '2test_kategorie'
        assert driver.find_element_by_id('item_2_datum').get_attribute('innerHTML') == 'Jan. 1, 2012'
        assert driver.find_element_by_id('item_2_wert').get_attribute('innerHTML') == '-2.00'
        assert driver.find_element_by_id('item_2_person').get_attribute('innerHTML') == 'test'
        driver.close()


    def teste_uebersicht_und_vorbelegung(self, driver_provider):
        driver = driver_provider()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_ausgabe(driver, '01012010', '0name', '0test_kategorie', '0.5', 'Maureen')
        define_kategorie(driver, '1test_kategorie')
        self._add_ausgabe(driver, '01012011', '1name', '1test_kategorie', 1, 'test')
        define_kategorie(driver, '2test_kategorie')
        self._add_ausgabe(driver, '01012012', '2name', '2test_kategorie', 2, 'test')
        self._add_ausgabe(driver, '01012013', '3name', '1test_kategorie', 3, 'Maureen')

        driver.get('http://localhost:8000/gemeinsameuebersicht/')

        assert driver.find_element_by_id('item_2_id').get_attribute('innerHTML') == '2'
        assert driver.find_element_by_id('item_2_name').get_attribute('innerHTML') == '2name'
        assert driver.find_element_by_id('item_2_kategorie').get_attribute('innerHTML') == '2test_kategorie'
        assert driver.find_element_by_id('item_2_datum').get_attribute('innerHTML') == 'Jan. 1, 2012'
        assert driver.find_element_by_id('item_2_wert').get_attribute('innerHTML') == '-2.00'

        sleep(2)
        edit_button = driver.find_element_by_id('edit_2')
        edit_button.click()

        assert driver.find_element_by_name('name').get_attribute('value') == '2name'
        assert get_selected_option(driver, 'kategorie_auswahl') == '2test_kategorie'
        assert driver.find_element_by_name('date').get_attribute('value') == '01/01/2012'
        assert driver.find_element_by_name('wert').get_attribute('value') == '2,00'


        driver.close()


