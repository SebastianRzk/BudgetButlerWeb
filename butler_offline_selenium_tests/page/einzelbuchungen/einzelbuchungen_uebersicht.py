from selenium.webdriver.common.by import By

from butler_offline_selenium_tests.page.util import select_option


class EinzelbuchungenUebersicht:
    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/uebersicht/')

    def open_module(self, month, year):
        month = str(month)
        if len(month) == 1:
            month = '0' + month

        open_table_button = self.driver.find_element(By.ID, 'open_{month}/{year}'.format(year=year, month=month))
        open_table_button.click()

    def open_year(self, year):
        select_option(self.driver, 'date', str(year))
        submit_button = self.driver.find_element(By.ID, 'set_date_button')
        submit_button.click()

    def get_item_in_opened_module(self, id):
        return {
            'name':  self.driver.find_element(By.ID, 'item_{id}_name'.format(id=id)).get_attribute('innerHTML'),
            'kategorie': self.driver.find_element(By.ID, 'item_{id}_kategorie'.format(id=id)).get_attribute('innerHTML'),
            'datum': self.driver.find_element(By.ID, 'item_{id}_datum'.format(id=id)).get_attribute('innerHTML'),
            'wert': self.driver.find_element(By.ID, 'item_{id}_wert'.format(id=id)).get_attribute('innerHTML')
        }

    def click_edit_button(self, id):
        edit_button = self.driver.find_element(By.ID, 'edit_{id}'.format(id=id))
        edit_button.click()
