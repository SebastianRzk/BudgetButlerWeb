from butler_offline_selenium_tests.page.util import fill_element, select_option, click_add_button, get_options, \
    get_selected_option
from selenium.webdriver.common.by import By


class GemeinsamAdd:

    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/addgemeinsam/')


    def add(self, date, name, kategorie, wert, person):
        fill_element(self.driver, 'date', date)
        fill_element(self.driver, 'name', name)
        fill_element(self.driver, 'wert', wert)
        select_option(self.driver, 'kategorie_auswahl', kategorie)
        select_option(self.driver, 'person_auswahl', person)

        click_add_button(driver=self.driver)

    def get_vorbelegung(self):
        return {
            'name': self.driver.find_element(By.NAME, 'name').get_attribute('value'),
            'kategorie': get_selected_option(self.driver, 'kategorie_auswahl'),
            'person': get_selected_option(self.driver, 'person_auswahl'),
            'datum': self.driver.find_element(By.NAME, 'date').get_attribute('value'),
            'wert': self.driver.find_element(By.NAME, 'wert').get_attribute('value')
        }

    def partner_options(self):
        return set(get_options(self.driver, 'person_auswahl'))
