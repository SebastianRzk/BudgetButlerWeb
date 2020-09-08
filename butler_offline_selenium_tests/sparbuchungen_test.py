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
        close_driver(driver)


'''
    def teste_edit_vorbelegung_ausgabe(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_sparbuchung(driver, '2010-01-01', '2010-02-02', '0name', '0test_kategorie', '0.5', 'Einnahme')
        define_kategorie(driver, '1test_kategorie')
        self._add_sparbuchung(driver, '2011-01-01', '2011-02-02', '1name', '1test_kategorie', 1, 'Ausgabe')
        define_kategorie(driver, '2test_kategorie')
        self._add_sparbuchung(driver, '2012-01-01', '2012-02-02', '2name', '2test_kategorie', 2, 'Ausgabe')
        self._add_sparbuchung(driver, '2013-01-01', '2013-02-02', '3name', '1test_kategorie', 3, 'Einnahme')

        driver.get('http://localhost:5000/dauerauftraguebersicht/')

        edit_button = driver.find_element_by_id('edit_2')
        edit_button.click()

        assert driver.find_element_by_name('name').get_attribute('value') == '2name'
        assert get_selected_option(driver, 'kategorie_auswahl') == '2test_kategorie'
        assert get_selected_option(driver, 'typ_auswahl') == 'Ausgabe'
        assert driver.find_element_by_name('startdatum').get_attribute('value') == '2012-01-01'
        assert driver.find_element_by_name('endedatum').get_attribute('value') == '2012-02-02'
        assert driver.find_element_by_name('wert').get_attribute('value') == '2,00'

        close_driver(driver)

    def teste_edit_vorbelegung_einnahme(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_sparbuchung(driver, '2010-01-01', '2010-02-02', '0name', '0test_kategorie', '0.5', 'Einnahme')
        define_kategorie(driver, '1test_kategorie')
        self._add_sparbuchung(driver, '2011-01-01', '2011-02-02', '1name', '1test_kategorie', 1, 'Ausgabe')
        define_kategorie(driver, '2test_kategorie')
        self._add_sparbuchung(driver, '2012-01-01', '2012-02-02', '2name', '2test_kategorie', 2, 'Ausgabe')
        self._add_sparbuchung(driver, '2013-01-01', '2013-02-02', '3name', '1test_kategorie', 3, 'Einnahme')

        driver.get('http://localhost:5000/dauerauftraguebersicht/')

        edit_button = driver.find_element_by_id('edit_0')
        edit_button.click()

        assert driver.find_element_by_name('name').get_attribute('value') == '0name'
        assert get_selected_option(driver, 'kategorie_auswahl') == '0test_kategorie'
        assert get_selected_option(driver, 'typ_auswahl') == 'Einnahme'
        assert driver.find_element_by_name('startdatum').get_attribute('value') == '2010-01-01'
        assert driver.find_element_by_name('endedatum').get_attribute('value') == '2010-02-02'
        assert driver.find_element_by_name('wert').get_attribute('value') == '0,50'

        close_driver(driver)

'''
