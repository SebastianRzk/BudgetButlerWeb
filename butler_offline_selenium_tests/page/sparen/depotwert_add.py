from butler_offline_selenium_tests.page.util import fill_element, select_option, click_add_button


class DepotwertAdd:
    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/add_depotwert/')

    def add(self, name, isin):
        fill_element(self.driver, 'name', name)
        fill_element(self.driver, 'isin', isin)
        select_option(self.driver, 'typ_auswahl', 'FOND')

        click_add_button(self.driver)
