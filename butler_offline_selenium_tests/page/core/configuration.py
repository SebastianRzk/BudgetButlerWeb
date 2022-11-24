from butler_offline_selenium_tests.SeleniumTest import fill_element
from selenium.webdriver.common.by import By


class Configuration:

    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://127.0.0.1:5000/configuration/')

    def define_kategorie(self, kategorie_name):
        fill_element(self.driver, 'neue_kategorie', kategorie_name)
        button = self.driver.find_element(By.ID, 'add_kategorie')
        button.click()
