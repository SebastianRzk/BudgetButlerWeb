from butler_offline_selenium_tests.page.util import fill_element, select_option, click_add_button, get_selected_option
from selenium.webdriver.common.by import By


class DauerauftragAdd:

    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/adddauerauftrag/')

    def add(self, startdatum, endedatum, name, kategorie, wert, typ, rhythmus='monatlich'):
        fill_element(self.driver, 'start_datum', startdatum)
        fill_element(self.driver, 'ende_datum', endedatum)
        fill_element(self.driver, 'name', name)
        fill_element(self.driver, 'wert', wert)
        select_option(self.driver, 'kategorie_auswahl', kategorie)
        select_option(self.driver, 'typ_auswahl', typ)
        select_option(self.driver, 'rhythmus_auswahl', rhythmus)
        click_add_button(self.driver)

    def get_vorbelegung(self):
        return {
            'name': self.driver.find_element(By.NAME, 'name').get_attribute('value'),
            'kategorie': get_selected_option(self.driver, 'kategorie_auswahl'),
            'typ': get_selected_option(self.driver, 'typ_auswahl'),
            'rhythmus': get_selected_option(self.driver, 'rhythmus_auswahl'),
            'startdatum': self.driver.find_element(By.NAME, 'start_datum').get_attribute('value'),
            'endedatum': self.driver.find_element(By.NAME, 'ende_datum').get_attribute('value'),
            'wert': self.driver.find_element(By.NAME, 'wert').get_attribute('value')
        }

    def click_split_button(self):
        split_button = self.driver.find_element(By.ID, 'preset_values')
        split_button.click()
