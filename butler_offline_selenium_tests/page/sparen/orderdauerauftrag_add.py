from butler_offline_selenium_tests.page.util import fill_element, select_option, click_add_button


class OrderDauerauftragAdd:

    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/add_orderdauerauftrag/')

    def add(self, startdatum, endedatum, name, depotwert, konto, wert, kauf):
        fill_element(self.driver, 'startdatum', startdatum)
        fill_element(self.driver, 'endedatum', endedatum)
        fill_element(self.driver, 'name', name)
        fill_element(self.driver, 'wert', wert)
        select_option(self.driver, 'konto_auswahl', konto)
        select_option(self.driver, 'depotwert_auswahl', depotwert)

        if kauf:
            select_option(self.driver, 'typ_auswahl', 'Kauf')
        else:
            select_option(self.driver, 'typ_auswahl', 'Verkauf')

        click_add_button(self.driver)
