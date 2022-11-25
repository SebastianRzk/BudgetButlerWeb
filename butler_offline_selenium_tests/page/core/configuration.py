from butler_offline_selenium_tests.page.util import fill_element
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

    def update_partnername(self, new_partner_name):
        fill_element(self.driver, 'partnername', new_partner_name)
        self.driver.find_element(By.ID, 'set_partnername').click()

    def update_theme_color(self, new_color):
        self.driver\
            .execute_script(
                "document.getElementById('themecolor').setAttribute('value', '{new_color}')".format(new_color=new_color))
        self.driver.find_element(By.ID, 'change_themecolor').click()
