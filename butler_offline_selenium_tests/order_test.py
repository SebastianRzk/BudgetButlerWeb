from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import enter_test_mode
from SeleniumTest import select_option
from SeleniumTest import click_add_button

class TestUI(SeleniumTestClass):
    def _add_depotwert(self, driver, name, isin):
        driver.get('http://localhost:5000/add_depotwert')
        fill_element(driver, 'name', name)
        fill_element(driver, 'isin', isin)
        click_add_button(driver)

    def _add_order(self, driver, datum, name, depotwert, konto, wert, kauf):
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

    def _add_orderdauerauftrag(self, driver, startdatum, endedatum, name, depotwert, konto, wert, kauf):
        driver.get('http://localhost:5000/add_orderdauerauftrag/')
        fill_element(driver, 'startdatum', startdatum)
        fill_element(driver, 'endedatum', endedatum)
        fill_element(driver, 'name', name)
        fill_element(driver, 'wert', wert)
        select_option(driver, 'konto_auswahl', konto)
        select_option(driver, 'depotwert_auswahl', depotwert)

        if kauf:
            select_option(driver, 'typ_auswahl', 'Kauf')
        else:
            select_option(driver, 'typ_auswahl', 'Verkauf')

        click_add_button(driver)

    def _add_depotauszug(self, driver, datum, konto, isin, wert):
        driver.get('http://localhost:5000/add_depotauszug/')
        fill_element(driver, 'datum_' + konto, datum)
        fill_element(driver, 'wert_' + konto + '_' + isin, wert)

        click_add_button(driver, '_' + konto)

    def _add_sparkonto(self, driver, name, typ):
        driver.get('http://localhost:5000/add_sparkonto/')
        fill_element(driver, 'kontoname', name)
        select_option(driver, 'typ_auswahl', typ)

        click_add_button(driver)


    def teste_uebersicht_kontos(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        self._add_sparkonto(driver, 'TestDepot', 'Depot')
        self._add_depotwert(driver, 'Depotwert1', 'Isin1')
        self._add_order(driver, '2020-01-01', 'first order', 'Isin1', 'TestDepot', 123, True)
        self._add_depotauszug(driver, '2020-01-01', 'TestDepot', 'Isin1', 124)

        driver.get('http://localhost:5000/uebersicht_sparkontos/')

        assert driver.find_element_by_id('item_0_id').get_attribute('innerHTML') == '0'
        assert driver.find_element_by_id('item_0_kontoname').get_attribute('innerHTML') == 'TestDepot'
        assert driver.find_element_by_id('item_0_kontotyp').get_attribute('innerHTML') == 'Depot'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '124,00'
        assert driver.find_element_by_id('item_0_aufbuchungen').get_attribute('innerHTML') == '123,00'
        assert driver.find_element_by_id('item_0_difference').get_attribute('innerHTML') == '1,00'


        assert driver.find_element_by_id('item_gesamt_wert').get_attribute('innerHTML') == '124,00'
        assert driver.find_element_by_id('item_gesamt_aufbuchungen').get_attribute('innerHTML') == '123,00'
        assert driver.find_element_by_id('item_gesamt_difference').get_attribute('innerHTML') == '1,00'
        close_driver(driver)


    def teste_orderdauerauftrag(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        self._add_sparkonto(driver, 'TestDepot', 'Depot')
        self._add_depotwert(driver, 'Depotwert1', 'Isin1')
        self._add_orderdauerauftrag(driver, '2020-01-01', '2020-02-02', 'first order', 'Isin1', 'TestDepot', 101, True)

        driver.get('http://localhost:5000/uebersicht_sparkontos/')

        assert driver.find_element_by_id('item_0_aufbuchungen').get_attribute('innerHTML') == '202,00'

        driver.get('http://localhost:5000/uebersicht_order')

        assert driver.find_element_by_id('item_0_datum').get_attribute('innerHTML') == '01.01.2020'
        assert driver.find_element_by_id('item_0_konto').get_attribute('innerHTML') == 'TestDepot'
        assert driver.find_element_by_id('item_0_depotwert').get_attribute('innerHTML') == 'Depotwert1 (Isin1)'
        assert driver.find_element_by_id('item_0_typ').get_attribute('innerHTML') == 'Kauf'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '101,00'

        assert driver.find_element_by_id('item_1_datum').get_attribute('innerHTML') == '01.02.2020'
        assert driver.find_element_by_id('item_1_konto').get_attribute('innerHTML') == 'TestDepot'
        assert driver.find_element_by_id('item_1_depotwert').get_attribute('innerHTML') == 'Depotwert1 (Isin1)'
        assert driver.find_element_by_id('item_1_typ').get_attribute('innerHTML') == 'Kauf'
        assert driver.find_element_by_id('item_1_wert').get_attribute('innerHTML') == '101,00'

        close_driver(driver)



