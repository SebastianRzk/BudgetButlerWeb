from selenium.webdriver.common.by import By

class EinzelbuchungenUebersicht:

    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/uebersicht/')

    def open_module(self, month, year):
        open_table_button = self.driver.find_element(By.ID, 'open_{year}.{month}'.format(year=year, month=month))
        open_table_button.click()

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
