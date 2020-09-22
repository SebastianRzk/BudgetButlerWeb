'''
Created on 23.11.2017

@author: sebastian
'''
from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import enter_test_mode
from SeleniumTest import select_option

class TestUI(SeleniumTestClass):
    def _add_sparbuchung(self, driver, datum, name, typ, konto, wert, einzahlung):
        driver.get('http://localhost:5000/add_sparbuchung/')
        fill_element(driver, 'datum', datum)
        fill_element(driver, 'name', name)
        fill_element(driver, 'wert', wert)
        select_option(driver, 'konto_auswahl', konto)
        select_option(driver, 'typ_auswahl', typ)

        if einzahlung:
            select_option(driver, 'eigenschaft_auswahl', 'Einzahlung')
        else:
            select_option(driver, 'eigenschaft_auswahl', 'Auszahlung')

        add_button = driver.find_element_by_id('add')
        add_button.click()

    def _add_sparkonto(self, driver, name, typ):
        driver.get('http://localhost:5000/add_sparkonto/')
        fill_element(driver, 'kontoname', name)
        select_option(driver, 'typ_auswahl', typ)

        add_button = driver.find_element_by_id('add')
        add_button.click()


    def teste_uebersicht_kontos(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        self._add_sparkonto(driver, 'TestKonto', 'Sparkonto')
        self._add_sparbuchung(driver, '2020-01-01', 'testname', 'Manueller Auftrag', 'TestKonto', 10,  True)

        driver.get('http://localhost:5000/uebersicht_sparkontos/')

        assert driver.find_element_by_id('item_0_id').get_attribute('innerHTML') == '0'
        assert driver.find_element_by_id('item_0_kontoname').get_attribute('innerHTML') == 'TestKonto'
        assert driver.find_element_by_id('item_0_kontotyp').get_attribute('innerHTML') == 'Sparkonto'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '10,00'
        assert driver.find_element_by_id('item_0_aufbuchungen').get_attribute('innerHTML') == '10,00'
        assert driver.find_element_by_id('item_0_difference').get_attribute('innerHTML') == '0,00'


        assert driver.find_element_by_id('item_gesamt_wert').get_attribute('innerHTML') == '10,00'
        assert driver.find_element_by_id('item_gesamt_aufbuchungen').get_attribute('innerHTML') == '10,00'
        assert driver.find_element_by_id('item_gesamt_difference').get_attribute('innerHTML') == '0,00'
        close_driver(driver)


    def teste_uebersicht_sparbuchungen(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        self._add_sparkonto(driver, 'TestKonto', 'Sparkonto')
        self._add_sparbuchung(driver, '2020-01-01', 'testname', 'Manueller Auftrag', 'TestKonto', 10,  True)

        driver.get('http://localhost:5000/uebersicht_sparbuchungen/')

        open_table_button = driver.find_element_by_id('open_2020.1')
        open_table_button.click()

        assert driver.find_element_by_id('item_0_id').get_attribute('innerHTML') == '0'
        assert driver.find_element_by_id('item_0_name').get_attribute('innerHTML') == 'testname'
        assert driver.find_element_by_id('item_0_konto').get_attribute('innerHTML') == 'TestKonto'
        assert driver.find_element_by_id('item_0_typ').get_attribute('innerHTML').strip() == 'Manueller Auftrag'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '10,00'


        driver.get('http://localhost:5000/uebersicht/')

        open_table_button = driver.find_element_by_id('open_2020.1')
        open_table_button.click()

        assert driver.find_element_by_id('item_0_id').get_attribute('innerHTML') == '0'
        assert driver.find_element_by_id('item_0_name').get_attribute('innerHTML') == 'testname'
        assert driver.find_element_by_id('item_0_kategorie').get_attribute('innerHTML') == 'Sparen'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '-10,00'
        close_driver(driver)

