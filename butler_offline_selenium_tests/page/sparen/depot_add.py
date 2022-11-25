from butler_offline_selenium_tests.page.util import fill_element, select_option, click_add_button


class DepotAdd:
    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/add_sparkonto/')

    def add(self, name, typ='Depot'):
        fill_element(self.driver, 'kontoname', name)
        select_option(self.driver, 'typ_auswahl', typ)

        click_add_button(self.driver)
