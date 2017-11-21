from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
from SeleniumTest import SeleniumTestClass


class TestUI(SeleniumTestClass):
    def _add_ausgabe(self, driver):
        driver.get('http://localhost:8000/addeinzelbuchung/')
        self._fill_element(driver, 'date', '17031994')
        self._fill_element(driver, 'name', 'eine ausgabe')
        self._fill_element(driver, 'wert', '12,34')
        add_button = driver.find_element_by_id('add')
        add_button.click()

        base_table = driver.find_element_by_id('letzte_erfassungen')
        tableRows = base_table.find_elements_by_tag_name('tr')
        print(tableRows[0].text)
        print(tableRows[1].text)

    def _enter_test_mode(self, driver):
        driver.get('http://localhost:8000/production/testmode')

    def _define_kategorie(self, driver):
        driver.get('http://127.0.0.1:8000/configuration/')
        kategorie_name = 'testkategorie'
        self._fill_element(driver, 'neue_kategorie', kategorie_name)
        button = driver.find_element_by_id('add_kategorie')
        button.click()

        self._look_for_kategorie_in_auswahl(driver, kategorie_name, 'http://localhost:8000/addeinzelbuchung/')
        self._look_for_kategorie_in_auswahl(driver, kategorie_name, 'http://localhost:8000/addeinnahme/')
        self._look_for_kategorie_in_auswahl(driver, kategorie_name, 'http://localhost:8000/adddauerauftrag/')

    def _look_for_kategorie_in_auswahl(self, driver, kategorie_name , link):
        driver.get(link)
        kategorie_auswahl = Select(driver.find_element_by_id('kategorie_auswahl'))

        assert kategorie_name in map(lambda x: x.text, kategorie_auswahl.options)


    def _fill_element(self, driver, elementname, content):
        elem = driver.find_element_by_name(elementname)
        elem.clear()
        elem.send_keys(content)



    def test_simple_example(self, driver_provider):
        DRIVER = driver_provider()
        self._enter_test_mode(DRIVER)

        self._define_kategorie(DRIVER)

        self._add_ausgabe(DRIVER)

        DRIVER.close()
