from butler_offline_selenium_tests.page.util import content_of, fill_element, select_option, fill_element_by_id
from selenium.webdriver.common.by import By


class GemeinsamAbrechnen:
    URL = 'http://localhost:5000/gemeinsamabrechnen/'

    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get(self.URL)

    def update_abrechnungsverhältnis(self, neues_verhaeltnis):
        fill_element_by_id(self.driver, 'abrechnungsverhaeltnis', str(neues_verhaeltnis))
        self.driver.find_element(By.ID, 'abrechnung_aktualisieren').click()

    def update_limit(self, person, value):
        self.driver.find_element(By.ID, 'set_limit').click()
        select_option(self.driver, 'set_limit_fuer', person)
        fill_element(self.driver, 'set_limit_value', str(value))
        self.driver.find_element(By.ID, 'abrechnung_aktualisieren').click()

    def set_self_kategorie(self, kategorie):
        self.driver.find_element(By.ID, 'set_self_kategorie').click()
        select_option(self.driver, 'set_self_kategorie_value', kategorie)
        self.driver.find_element(By.ID, 'abrechnung_aktualisieren').click()

    def set_other_kategorie(self, kategorie):
        self.driver.find_element(By.ID, 'set_other_kategorie').click()
        fill_element_by_id(self.driver, 'set_other_kategorie_value', kategorie)
        self.driver.find_element(By.ID, 'abrechnung_aktualisieren').click()

    def abrechnen(self):
        self.driver.find_element(By.ID, 'abrechnen').click()

    def result_self(self):
        return {
            'ausgabe_self': content_of(self.driver, 'ausgabe_self'),
            'ausgabe_self_soll': content_of(self.driver, 'ausgabe_self_soll'),
            'ausgabe_self_diff': content_of(self.driver, 'ausgabe_self_diff'),
        }

    def result_partner(self):
        return {
            'ausgabe_partner': content_of(self.driver, 'ausgabe_partner'),
            'ausgabe_partner_soll': content_of(self.driver, 'ausgabe_partner_soll'),
            'ausgabe_partner_diff': content_of(self.driver, 'ausgabe_partner_diff'),
        }

    def abrechnung_result(self) -> str:
        return content_of(self.driver, 'abrechnung').replace('<br>', '\n').strip()

