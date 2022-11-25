from selenium.webdriver.common.by import By


class Menu:
    def __init__(self, driver):
        self.driver = driver

    def change_database(self, database_name):
        self.driver\
            .get('http://localhost:5000/production/?database={database_name}'.format(database_name=database_name))

    def get_title(self):
        return self.driver.find_element(By.CLASS_NAME, 'info')\
                   .find_element(By.TAG_NAME, 'strong').get_attribute('innerHTML')


