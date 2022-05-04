from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import enter_test_mode
from SeleniumTest import select_option
from SeleniumTest import click_add_button

class TestUI(SeleniumTestClass):
    def _add_order(self, driver, datum, name, depotwert, konto, wert, kauf=True):
        driver.get('http://localhost:5000/add_order/')
        fill_element(driver, 'datum', datum)
        fill_element(driver, 'name', name)
        fill_element(driver, 'wert', wert)
        select_option(driver, 'konto_auswahl', konto)
        select_option(driver, 'depotwert_auswahl', depotwert)

        if kauf:
            select_option(driver, 'typ_auswahl', 'Kauf')
        else:
            select_option(driver, 'typ_auswahl', 'Verkauf')

        click_add_button(driver)

    def _add_depot(self, driver, name):
        driver.get('http://localhost:5000/add_sparkonto/')
        fill_element(driver, 'kontoname', name)
        select_option(driver, 'typ_auswahl', 'Depot')

        click_add_button(driver)

    def _add_depotwert(self, driver, name, isin):
        driver.get('http://localhost:5000/add_depotwert/')
        fill_element(driver, 'name', name)
        fill_element(driver, 'isin', isin)
        select_option(driver, 'typ_auswahl', 'FOND')

        click_add_button(driver)

    def _add_depotauszug(self, driver, datum, konto, depotwert, wert):
        driver.get('http://localhost:5000/add_depotauszug/')
        fill_element(driver, 'datum_' + konto, datum)
        fill_element(driver, 'wert_' + konto + '_' + depotwert, wert)

        click_add_button(driver, '_' + konto)


    def teste_uebersicht_order(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        self._add_depot(driver, 'Testdepot')
        self._add_depotwert(driver, 'Testdepotwert', 'ISINDEMO')
        self._add_order(driver, '2020-01-01', 'testname', 'Testdepotwert (ISINDEMO)', 'Testdepot', 10,  True)

        driver.get('http://localhost:5000/uebersicht_order/')

        assert driver.find_element_by_id('item_0_datum').get_attribute('innerHTML') == '01.01.2020'
        assert driver.find_element_by_id('item_0_name').get_attribute('innerHTML') == 'testname'
        assert driver.find_element_by_id('item_0_depotwert').get_attribute('innerHTML') == 'Testdepotwert (ISINDEMO)'
        assert driver.find_element_by_id('item_0_konto').get_attribute('innerHTML') == 'Testdepot'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '10,00'
        close_driver(driver)

    def teste_uebersicht_kontos(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        self._add_depot(driver, 'TestKonto')
        self._add_depotwert(driver, 'Testdepotwert', 'ISINDEMO')
        self._add_order(driver, '2020-01-01', 'testname', 'Testdepotwert (ISINDEMO)', 'Testdepot', 10,  True)
        self._add_depotauszug(driver, '2020-01-02', 'TestKonto', 'ISINDEMO', 9)


        driver.get('http://localhost:5000/uebersicht_sparkontos/')

        assert driver.find_element_by_id('item_0_id').get_attribute('innerHTML') == '0'
        assert driver.find_element_by_id('item_0_kontoname').get_attribute('innerHTML') == 'TestKonto'
        assert driver.find_element_by_id('item_0_kontotyp').get_attribute('innerHTML') == 'Depot'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '9,00'
        assert driver.find_element_by_id('item_0_aufbuchungen').get_attribute('innerHTML') == '10,00'
        assert driver.find_element_by_id('item_0_difference').get_attribute('innerHTML') == '-1,00'
        close_driver(driver)

    def teste_uebersicht_depotwerte(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        self._add_depotwert(driver, 'Testdepotwert', 'ISINDEMO')

        driver.get('http://localhost:5000/uebersicht_depotwerte/')

        assert driver.find_element_by_id('item_0_id').get_attribute('innerHTML') == '0'
        assert driver.find_element_by_id('item_0_name').get_attribute('innerHTML') == 'Testdepotwert'
        assert driver.find_element_by_id('item_0_isin').get_attribute('innerHTML') == 'ISINDEMO'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '0,00'
        close_driver(driver)



