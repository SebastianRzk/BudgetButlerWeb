from butler_offline_selenium_tests.page.util import fill_element, select_option, click_add_button, get_selected_option
from selenium.webdriver.common.by import By


class EinzelbuchungAdd:

    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/addausgabe/')

    def add(self, date, name, kategorie, wert):
        fill_element(self.driver, 'date', date)
        fill_element(self.driver, 'name', name)
        fill_element(self.driver, 'wert', wert)
        select_option(self.driver, 'kategorie_auswahl', kategorie)

        click_add_button(self.driver)

    def get_vorbelegung(self):
        return {
            'name': self.driver.find_element(By.NAME, 'name').get_attribute('value'),
            'kategorie': get_selected_option(self.driver, 'kategorie_auswahl'),
            'datum': self.driver.find_element(By.NAME, 'date').get_attribute('value'),
            'wert': self.driver.find_element(By.NAME, 'wert').get_attribute('value'),
        }

    def add_button_color(self):
        add_button = self.driver.find_element(By.ID, 'add')
        return add_button.value_of_css_property("background-color")

    