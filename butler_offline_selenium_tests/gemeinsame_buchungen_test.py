from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import enter_test_mode
from SeleniumTest import define_kategorie
from SeleniumTest import select_option
from SeleniumTest import get_selected_option


class TestUI(SeleniumTestClass):
    def _add_ausgabe(self, driver, date, name, kategorie, wert, person):
        driver.get('http://localhost:5000/addgemeinsam/')
        fill_element(driver, 'date', date)
        fill_element(driver, 'name', name)
        fill_element(driver, 'wert', wert)
        select_option(driver, 'kategorie_auswahl', kategorie)
        select_option(driver, 'person_auswahl', person)


        add_button = driver.find_element_by_id('add')
        add_button.click()

    def teste_uebersicht(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_ausgabe(driver, '2010-01-01', '0name', '0test_kategorie', '0.5', 'Partner')
        define_kategorie(driver, '1test_kategorie')
        self._add_ausgabe(driver, '2011-01-01', '1name', '1test_kategorie', 1, 'test')
        define_kategorie(driver, '2test_kategorie')
        self._add_ausgabe(driver, '2012-01-01', '2name', '2test_kategorie', 2, 'test')
        self._add_ausgabe(driver, '2013-01-01', '3name', '1test_kategorie', 3, 'Partner')

        driver.get('http://localhost:5000/gemeinsameuebersicht/')

        assert driver.find_element_by_id('item_2_id').get_attribute('innerHTML') == '2'
        assert driver.find_element_by_id('item_2_name').get_attribute('innerHTML') == '2name'
        assert driver.find_element_by_id('item_2_kategorie').get_attribute('innerHTML') == '2test_kategorie'
        assert driver.find_element_by_id('item_2_datum').get_attribute('innerHTML') == '01.01.2012'
        assert driver.find_element_by_id('item_2_wert').get_attribute('innerHTML') == '-2,00'
        assert driver.find_element_by_id('item_2_person').get_attribute('innerHTML') == 'test'

        close_driver(driver)

    def teste_vorbelegung_with_self(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_ausgabe(driver, '2010-01-01', '0name', '0test_kategorie', '0.5', 'Partner')
        define_kategorie(driver, '1test_kategorie')
        self._add_ausgabe(driver, '2011-01-01', '1name', '1test_kategorie', 1, 'test')
        define_kategorie(driver, '2test_kategorie')
        self._add_ausgabe(driver, '2012-01-01', '2name', '2test_kategorie', 2, 'test')
        self._add_ausgabe(driver, '2013-01-01', '3name', '1test_kategorie', 3, 'Partner')

        driver.get('http://localhost:5000/gemeinsameuebersicht/')

        edit_button = driver.find_element_by_id('edit_2')
        edit_button.click()

        assert driver.find_element_by_name('name').get_attribute('value') == '2name'
        assert get_selected_option(driver, 'kategorie_auswahl') == '2test_kategorie'
        assert get_selected_option(driver, 'person_auswahl') == 'test'
        assert driver.find_element_by_name('date').get_attribute('value') == '2012-01-01'
        assert driver.find_element_by_name('wert').get_attribute('value') == '2,00'

        close_driver(driver)

    def teste_vorbelegung_with_other(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_ausgabe(driver, '2010-01-01', '0name', '0test_kategorie', '0.5', 'Partner')
        define_kategorie(driver, '1test_kategorie')
        self._add_ausgabe(driver, '2011-01-01', '1name', '1test_kategorie', 1, 'test')
        define_kategorie(driver, '2test_kategorie')
        self._add_ausgabe(driver, '2012-01-01', '2name', '2test_kategorie', 2, 'test')
        self._add_ausgabe(driver, '2013-01-01', '3name', '1test_kategorie', 3, 'Partner')

        driver.get('http://localhost:5000/gemeinsameuebersicht/')

        edit_button = driver.find_element_by_id('edit_0')
        edit_button.click()

        assert driver.find_element_by_name('name').get_attribute('value') == '0name'
        assert get_selected_option(driver, 'kategorie_auswahl') == '0test_kategorie'
        assert get_selected_option(driver, 'person_auswahl') == 'Partner'
        assert driver.find_element_by_name('date').get_attribute('value') == '2010-01-01'
        assert driver.find_element_by_name('wert').get_attribute('value') == '0,50'

        close_driver(driver)



