from selenium.webdriver.common.by import By


class SparbuchungUebersicht:

    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/uebersicht_sparbuchungen/')

    def get(self, id):
        return {
            'name': self.driver.find_element(By.ID, 'item_{id}_name'.format(id=id)).get_attribute('innerHTML'),
            'konto': self.driver.find_element(By.ID, 'item_{id}_konto'.format(id=id)).get_attribute('innerHTML'),
            'wert': self.driver.find_element(By.ID, 'item_{id}_wert'.format(id=id)).get_attribute('innerHTML'),
            'typ': self.driver.find_element(By.ID, 'item_{id}_typ'.format(id=id)).get_attribute('innerHTML').strip  (),
        }

    def open_module(self, month, year):
        open_table_button = self.driver.find_element(By.ID, 'open_{year}.{month}'.format(year=year, month=month))
        open_table_button.click()

