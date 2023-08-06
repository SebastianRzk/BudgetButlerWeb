from butler_offline_selenium_tests.page.util import fill_element, select_option, get_selected_option, pagename
from selenium.webdriver.common.by import By


class Import:
    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/import/')

    def import_data(self, data):
        fill_element(self.driver, 'import', data)
        self.driver.find_element(By.NAME, 'btn_import').click()

    def page_name(self):
        return pagename(self.driver)

    def click_action(self):
        self.driver.find_element(By.NAME, 'action').click()

    def get_message(self):
        return self.driver.find_element(By.ID, 'message-box-content').get_attribute('innerHTML')

    def select_mapping(self, source_kategorie, destination_kategorie):
        select_option(self.driver,
                      '{source}_mapping'.format(source=source_kategorie),
                      'als {destination} importieren'.format(destination=destination_kategorie))


