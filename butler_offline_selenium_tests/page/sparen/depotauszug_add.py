from butler_offline_selenium_tests.page.util import fill_element_by_id, click_add_button, click_open_more_button


class DepotauszugAdd:
    def __init__(self, driver):
        self.driver = driver

    def add(self, datum, konto, depotwert, wert):
        fill_element_by_id(self.driver, 'edit_datum_' + konto, datum)
        fill_element_by_id(self.driver, 'edit_wert_new_' + konto + '_' + depotwert, wert)

        click_add_button(self.driver, '_' + konto)

    def open_weitere_depotwerte(self, konto):
        click_open_more_button(self.driver, "add_depotauszug_" + konto)

    def visit(self):
        self.driver.get('http://localhost:5000/add_depotauszug/')
