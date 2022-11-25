from butler_offline_selenium_tests.page.util import fill_element, select_option, click_add_button


class SparbuchungAdd:
    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/add_sparbuchung/')

    def add(self, datum, name, typ, konto, wert, einzahlung):
        fill_element(self.driver, 'datum', datum)
        fill_element(self.driver, 'name', name)
        fill_element(self.driver, 'wert', wert)
        select_option(self.driver, 'konto_auswahl', konto)
        select_option(self.driver, 'typ_auswahl', typ)

        if einzahlung:
            select_option(self.driver, 'eigenschaft_auswahl', 'Einzahlung')
        else:
            select_option(self.driver, 'eigenschaft_auswahl', 'Auszahlung')

        click_add_button(self.driver)
