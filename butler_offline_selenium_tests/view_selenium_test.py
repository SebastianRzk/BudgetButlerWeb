from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import enter_test_mode
from SeleniumTest import define_kategorie
from SeleniumTest import click_add_button


class TestUI(SeleniumTestClass):
    def _add_ausgabe(self, driver):
        driver.get('http://localhost:5000/addausgabe/')
        fill_element(driver, 'date', '17031994')
        fill_element(driver, 'name', 'eine ausgabe')
        fill_element(driver, 'wert', '12,34')
        click_add_button(driver)

        base_table = driver.find_element_by_id('letzte_erfassungen')
        tableRows = base_table.find_elements_by_tag_name('tr')


    def _define_kategorie(self, driver):
        kategorie_name = 'testkategorie'
        define_kategorie(driver, kategorie_name)

        self._look_for_kategorie_in_auswahl(driver, kategorie_name, 'http://localhost:5000/addausgabe/')
        self._look_for_kategorie_in_auswahl(driver, kategorie_name, 'http://localhost:5000/addeinnahme/')
        self._look_for_kategorie_in_auswahl(driver, kategorie_name, 'http://localhost:5000/adddauerauftrag/')

    def _look_for_kategorie_in_auswahl(self, driver, kategorie_name , link):
        driver.get(link)
        kategorie_auswahl = Select(driver.find_element_by_id('kategorie_auswahl'))

        assert kategorie_name in map(lambda x: x.text, kategorie_auswahl.options)


    def test_simple_example(self, get_driver, close_driver):
        DRIVER = get_driver()
        enter_test_mode(DRIVER)

        self._define_kategorie(DRIVER)

        self._add_ausgabe(DRIVER)

        close_driver(DRIVER)
