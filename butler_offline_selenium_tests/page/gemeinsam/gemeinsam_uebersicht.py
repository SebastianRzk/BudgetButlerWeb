from selenium.webdriver.common.by import By


class GemeinsamUeberischt:
    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/gemeinsameuebersicht/')

    def get_row(self, id):
        return {
            'name': self.driver.find_element(By.ID, 'item_{id}_name'.format(id=id)).get_attribute('innerHTML'),
            'kategorie': self.driver.find_element(By.ID, 'item_{id}_kategorie'.format(id=id)).get_attribute('innerHTML'),
            'datum': self.driver.find_element(By.ID, 'item_{id}_datum'.format(id=id)).get_attribute('innerHTML'),
            'wert': self.driver.find_element(By.ID, 'item_{id}_wert'.format(id=id)).get_attribute('innerHTML'),
            'person': self.driver.find_element(By.ID, 'item_{id}_person'.format(id=id)).get_attribute('innerHTML')
        }

    def click_edit_button(self, id):
        edit_button = self.driver.find_element(By.ID, 'edit_{id}'.format(id=id))
        edit_button.click()
