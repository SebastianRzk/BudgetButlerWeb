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
    def _add_dauerauftrag(self, driver, startdatum, endedatum, name, kategorie, wert, typ):
        driver.get('http://localhost:8000/adddauerauftrag/')
        fill_element(driver, 'startdatum', startdatum)
        fill_element(driver, 'endedatum', endedatum)
        fill_element(driver, 'name', name)
        fill_element(driver, 'wert', wert)
        select_option(driver, 'kategorie_auswahl', kategorie)
        select_option(driver, 'typ_auswahl', typ)

        add_button = driver.find_element_by_id('add')
        add_button.click()


    def teste_uebersicht(self, driver_provider):
        driver = driver_provider()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_dauerauftrag(driver, '01012010', '02022010', '0name', '0test_kategorie', '0.5', 'Einnahme')
        define_kategorie(driver, '1test_kategorie')
        self._add_dauerauftrag(driver, '01012011', '02022011', '1name', '1test_kategorie', 1, 'Ausgabe')
        define_kategorie(driver, '2test_kategorie')
        self._add_dauerauftrag(driver, '01012012', '02022012', '2name', '2test_kategorie', 2, 'Ausgabe')
        self._add_dauerauftrag(driver, '01012013', '02022013', '3name', '1test_kategorie', 3, 'Einnahme')

        driver.get('http://localhost:8000/dauerauftraguebersicht/')

        assert driver.find_element_by_id('item_2_id').get_attribute('innerHTML') == '2'
        assert driver.find_element_by_id('item_2_name').get_attribute('innerHTML') == '2name'
        assert driver.find_element_by_id('item_2_kategorie').get_attribute('innerHTML') == '2test_kategorie'
        assert driver.find_element_by_id('item_2_startdatum').get_attribute('innerHTML') == 'Jan. 1, 2012'
        assert driver.find_element_by_id('item_2_endedatum').get_attribute('innerHTML') == 'Feb. 2, 2012'
        assert driver.find_element_by_id('item_2_wert').get_attribute('innerHTML') == '-2.00'


    def teste_edit_vorbelegung_ausgabe(self, driver_provider):
        driver = driver_provider()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_dauerauftrag(driver, '01012010', '02022010', '0name', '0test_kategorie', '0.5', 'Einnahme')
        define_kategorie(driver, '1test_kategorie')
        self._add_dauerauftrag(driver, '01012011', '02022011', '1name', '1test_kategorie', 1, 'Ausgabe')
        define_kategorie(driver, '2test_kategorie')
        self._add_dauerauftrag(driver, '01012012', '02022012', '2name', '2test_kategorie', 2, 'Ausgabe')
        self._add_dauerauftrag(driver, '01012013', '02022013', '3name', '1test_kategorie', 3, 'Einnahme')

        driver.get('http://localhost:8000/dauerauftraguebersicht/')

        edit_button = driver.find_element_by_id('edit_2')
        edit_button.click()

        assert driver.find_element_by_name('name').get_attribute('value') == '2name'
        assert get_selected_option(driver, 'kategorie_auswahl') == '2test_kategorie'
        assert get_selected_option(driver, 'typ_auswahl') == 'Ausgabe'
        assert driver.find_element_by_name('startdatum').get_attribute('value') == '01.01.2012'
        assert driver.find_element_by_name('endedatum').get_attribute('value') == '02.02.2012'
        assert driver.find_element_by_name('wert').get_attribute('value') == '2,00'

        driver.close()

    def teste_edit_vorbelegung_einnahme(self, driver_provider):
        driver = driver_provider()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_dauerauftrag(driver, '01012010', '02022010', '0name', '0test_kategorie', '0.5', 'Einnahme')
        define_kategorie(driver, '1test_kategorie')
        self._add_dauerauftrag(driver, '01012011', '02022011', '1name', '1test_kategorie', 1, 'Ausgabe')
        define_kategorie(driver, '2test_kategorie')
        self._add_dauerauftrag(driver, '01012012', '02022012', '2name', '2test_kategorie', 2, 'Ausgabe')
        self._add_dauerauftrag(driver, '01012013', '02022013', '3name', '1test_kategorie', 3, 'Einnahme')

        driver.get('http://localhost:8000/dauerauftraguebersicht/')

        edit_button = driver.find_element_by_id('edit_0')
        edit_button.click()

        assert driver.find_element_by_name('name').get_attribute('value') == '0name'
        assert get_selected_option(driver, 'kategorie_auswahl') == '0test_kategorie'
        assert get_selected_option(driver, 'typ_auswahl') == 'Einnahme'
        assert driver.find_element_by_name('startdatum').get_attribute('value') == '01.01.2010'
        assert driver.find_element_by_name('endedatum').get_attribute('value') == '02.02.2010'
        assert driver.find_element_by_name('wert').get_attribute('value') == '0,50'

        driver.close()

