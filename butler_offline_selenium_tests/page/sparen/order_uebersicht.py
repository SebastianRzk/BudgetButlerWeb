from selenium.webdriver.common.by import By


class OrderUebersicht:
    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/uebersicht_order/')

    def get(self, id):
        return {
            'datum': self.driver.find_element(By.ID, 'item_{id}_datum'.format(id=id)).get_attribute('innerHTML'),
            'name': self.driver.find_element(By.ID, 'item_{id}_name'.format(id=id)).get_attribute('innerHTML'),
            'depotwert': self.driver.find_element(By.ID, 'item_{id}_depotwert'.format(id=id)).get_attribute('innerHTML'),
            'konto': self.driver.find_element(By.ID, 'item_{id}_konto'.format(id=id)).get_attribute('innerHTML'),
            'wert': self.driver.find_element(By.ID, 'item_{id}_wert'.format(id=id)).get_attribute('innerHTML')
        }
