from selenium.webdriver.common.by import By


class DepotwertUebersicht:
    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/uebersicht_depotwerte/')

    def get(self, id):
        return {
            'name': self.driver.find_element(By.ID, 'item_{id}_name'.format(id=id)).get_attribute('innerHTML'),
            'isin': self.driver.find_element(By.ID, 'item_{id}_isin'.format(id=id)).get_attribute('innerHTML'),
            'wert': self.driver.find_element(By.ID, 'item_{id}_wert'.format(id=id)).get_attribute('innerHTML'),
        }
