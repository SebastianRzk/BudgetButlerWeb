from selenium.webdriver.common.by import By

class DauerauftragUebersicht:

    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/dauerauftraguebersicht/')

    def get_row(self, id):
        return {
            'id': self.driver.find_element(By.ID, 'item_{id}_id'.format(id=id)).get_attribute('innerHTML'),
            'name': self.driver.find_element(By.ID, 'item_{id}_name'.format(id=id)).get_attribute('innerHTML'),
            'kategorie': self.driver.find_element(By.ID, 'item_{id}_kategorie'.format(id=id)).get_attribute('innerHTML'),
            'startdatum': self.driver.find_element(By.ID, 'item_{id}_startdatum'.format(id=id)).get_attribute('innerHTML'),
            'endedatum': self.driver.find_element(By.ID, 'item_{id}_endedatum'.format(id=id)).get_attribute('innerHTML'),
            'wert': self.driver.find_element(By.ID, 'item_{id}_wert'.format(id=id)).get_attribute('innerHTML'),
        }

    def click_edit_button(self, id):
        edit_button = self.driver.find_element(By.ID, 'edit_{id}'.format(id=id))
        edit_button.click()

