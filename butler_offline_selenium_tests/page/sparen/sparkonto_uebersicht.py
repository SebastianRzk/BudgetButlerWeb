from selenium.webdriver.common.by import By


class SparkontoUebersicht:

    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/uebersicht_sparkontos/')

    def get(self, id):
        return {
            'name': self.driver.find_element(By.ID, 'item_{id}_kontoname'.format(id=id)).get_attribute('innerHTML'),
            'typ': self.driver.find_element(By.ID, 'item_{id}_kontotyp'.format(id=id)).get_attribute('innerHTML'),
            'wert': self.driver.find_element(By.ID, 'item_{id}_wert'.format(id=id)).get_attribute('innerHTML'),
            'aufbuchungen': self.driver.find_element(By.ID, 'item_{id}_aufbuchungen'.format(id=id)).get_attribute('innerHTML'),
            'difference': self.driver.find_element(By.ID, 'item_{id}_difference'.format(id=id)).get_attribute('innerHTML'),
        }

