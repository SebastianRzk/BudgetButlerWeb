from butler_offline_selenium_tests.page.util import fill_element, select_option
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
        self.driver \
            .execute_script(
            "document.getElementById('themecolor').setAttribute('value', '{new_color}')".format(new_color=new_color))
        self.driver.find_element(By.ID, 'change_themecolor').click()

    def click_on_backup(self):
        self.driver.find_element(By.ID, 'create_backup').click()

    def get_page_message(self) -> str:
        return self.driver.find_element(By.ID, 'message-box-content').get_attribute('innerHTML')

    def rename(self, kategorie_alt: str, kategorie_neu: str):
        select_option(driver=self.driver,
                      option_id='kategorie_rename_alt',
                      item=kategorie_alt
                      )
        fill_element(driver=self.driver,
                     elementname='kategorie_neu',
                     content=kategorie_neu
                     )
        button = self.driver.find_element(By.ID, 'rename_kategorie')
        button.click()
