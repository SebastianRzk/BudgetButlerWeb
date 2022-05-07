from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import enter_test_mode
from SeleniumTest import define_kategorie
from SeleniumTest import select_option
from SeleniumTest import get_selected_option
from SeleniumTest import click_add_button


class TestUI(SeleniumTestClass):
    def _add_dauerauftrag(self, driver, startdatum, endedatum, name, kategorie, wert, typ, rhythmus='monatlich'):
        driver.get('http://localhost:5000/adddauerauftrag/')
        fill_element(driver, 'startdatum', startdatum)
        fill_element(driver, 'endedatum', endedatum)
        fill_element(driver, 'name', name)
        fill_element(driver, 'wert', wert)
        select_option(driver, 'kategorie_auswahl', kategorie)
        select_option(driver, 'typ_auswahl', typ)
        select_option(driver, 'rhythmus_auswahl', rhythmus)

        click_add_button(driver)


    def teste_uebersicht(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_dauerauftrag(driver, '2010-01-01', '2010-02-02', '0name', '0test_kategorie', '0.5', 'Einnahme')
        define_kategorie(driver, '1test_kategorie')
        self._add_dauerauftrag(driver, '2011-01-01', '2011-02-02', '1name', '1test_kategorie', 1, 'Ausgabe')
        define_kategorie(driver, '2test_kategorie')
        self._add_dauerauftrag(driver, '2012-01-01', '2012-02-02', '2name', '2test_kategorie', 2, 'Ausgabe')
        self._add_dauerauftrag(driver, '2013-01-01', '2013-02-02', '3name', '1test_kategorie', 3, 'Einnahme')

        driver.get('http://localhost:5000/dauerauftraguebersicht/')

        assert driver.find_element_by_id('item_2_id').get_attribute('innerHTML') == '2'
        assert driver.find_element_by_id('item_2_name').get_attribute('innerHTML') == '2name'
        assert driver.find_element_by_id('item_2_kategorie').get_attribute('innerHTML') == '2test_kategorie'
        assert driver.find_element_by_id('item_2_startdatum').get_attribute('innerHTML') == '01.01.2012'
        assert driver.find_element_by_id('item_2_endedatum').get_attribute('innerHTML') == '02.02.2012'
        assert driver.find_element_by_id('item_2_wert').get_attribute('innerHTML') == '-2.00'
        close_driver(driver)


    def teste_edit_vorbelegung_ausgabe(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_dauerauftrag(driver, '2010-01-01', '2010-02-02', '0name', '0test_kategorie', '0.5', 'Einnahme')
        define_kategorie(driver, '1test_kategorie')
        self._add_dauerauftrag(driver, '2011-01-01', '2011-02-02', '1name', '1test_kategorie', 1, 'Ausgabe')
        define_kategorie(driver, '2test_kategorie')
        self._add_dauerauftrag(
            driver, '2012-01-01', '2012-02-02', '2name', '2test_kategorie', 2, 'Ausgabe', rhythmus='jaehrlich')
        self._add_dauerauftrag(driver, '2013-01-01', '2013-02-02', '3name', '1test_kategorie', 3, 'Einnahme')

        driver.get('http://localhost:5000/dauerauftraguebersicht/')

        edit_button = driver.find_element_by_id('edit_2')
        edit_button.click()

        assert driver.find_element_by_name('name').get_attribute('value') == '2name'
        assert get_selected_option(driver, 'kategorie_auswahl') == '2test_kategorie'
        assert get_selected_option(driver, 'typ_auswahl') == 'Ausgabe'
        assert get_selected_option(driver, 'rhythmus_auswahl') == 'jaehrlich'
        assert driver.find_element_by_name('startdatum').get_attribute('value') == '2012-01-01'
        assert driver.find_element_by_name('endedatum').get_attribute('value') == '2012-02-02'
        assert driver.find_element_by_name('wert').get_attribute('value') == '2,00'

        close_driver(driver)

    def teste_edit_vorbelegung_einnahme(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_dauerauftrag(driver, '2010-01-01', '2010-02-02', '0name', '0test_kategorie', '0.5', 'Einnahme')
        define_kategorie(driver, '1test_kategorie')
        self._add_dauerauftrag(driver, '2011-01-01', '2011-02-02', '1name', '1test_kategorie', 1, 'Ausgabe')
        define_kategorie(driver, '2test_kategorie')
        self._add_dauerauftrag(driver, '2012-01-01', '2012-02-02', '2name', '2test_kategorie', 2, 'Ausgabe')
        self._add_dauerauftrag(driver, '2013-01-01', '2013-02-02', '3name', '1test_kategorie', 3, 'Einnahme')

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

    def teste_vierteljaehrlich(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '2test_kategorie')
        self._add_dauerauftrag(
            driver, '2010-01-31', '2011-08-02', '2name', '2test_kategorie', 2, 'Ausgabe', rhythmus='vierteljaehrlich')

        driver.get('http://localhost:5000/uebersicht/')

        open_table_button = driver.find_element_by_id('open_2010.1')
        open_table_button.click()

        assert driver.find_element_by_id('item_0_name').get_attribute('innerHTML') == '2name'
        assert driver.find_element_by_id('item_0_kategorie').get_attribute('innerHTML') == '2test_kategorie'
        assert driver.find_element_by_id('item_0_datum').get_attribute('innerHTML') == '31.01.2010'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '-2,00'

        open_table_button = driver.find_element_by_id('open_2010.4')
        open_table_button.click()

        assert driver.find_element_by_id('item_1_name').get_attribute('innerHTML') == '2name'
        assert driver.find_element_by_id('item_1_kategorie').get_attribute('innerHTML') == '2test_kategorie'
        assert driver.find_element_by_id('item_1_datum').get_attribute('innerHTML') == '30.04.2010'
        assert driver.find_element_by_id('item_1_wert').get_attribute('innerHTML') == '-2,00'

        open_table_button = driver.find_element_by_id('open_2010.7')
        open_table_button.click()

        assert driver.find_element_by_id('item_2_name').get_attribute('innerHTML') == '2name'
        assert driver.find_element_by_id('item_2_kategorie').get_attribute('innerHTML') == '2test_kategorie'
        assert driver.find_element_by_id('item_2_datum').get_attribute('innerHTML') == '31.07.2010'
        assert driver.find_element_by_id('item_2_wert').get_attribute('innerHTML') == '-2,00'

        close_driver(driver)

