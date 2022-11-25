from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import enter_test_mode
from butler_offline_selenium_tests.page.sparen.order_add import OrderAdd
from butler_offline_selenium_tests.page.sparen.depot_add import DepotAdd
from butler_offline_selenium_tests.page.sparen.depotwert_add import DepotwertAdd
from butler_offline_selenium_tests.page.sparen.order_uebersicht import OrderUebersicht
from butler_offline_selenium_tests.page.sparen.depotauszug_add import DepotauszugAdd
from butler_offline_selenium_tests.page.sparen.depot_uebersicht import DepotUebersicht
from butler_offline_selenium_tests.page.sparen.depotwert_uebersicht import DepotwertUebersicht


class TestUI(SeleniumTestClass):

    def teste_uebersicht_order(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_order_add = OrderAdd(driver=driver)
        page_depot_add = DepotAdd(driver=driver)
        page_depotwert_add = DepotwertAdd(driver=driver)
        page_order_uebersicht = OrderUebersicht(driver=driver)

        page_depot_add.visit()
        page_depot_add.add('Testdepot')

        page_depotwert_add.visit()
        page_depotwert_add.add('Testdepotwert', 'ISINDEMO')
        page_order_add.visit()
        page_order_add.add('2020-01-01', 'testname', 'Testdepotwert (ISINDEMO)', 'Testdepot', 10,  True)

        page_order_uebersicht.visit()

        assert page_order_uebersicht.get(0) == {
            'datum': '01.01.2020',
            'name': 'testname',
            'depotwert': 'Testdepotwert (ISINDEMO)',
            'konto': 'Testdepot',
            'wert': '10,00'
        }
        close_driver(driver)

    def teste_uebersicht_kontos(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_order_add = OrderAdd(driver=driver)
        page_depot_add = DepotAdd(driver=driver)
        page_depotwert_add = DepotwertAdd(driver=driver)
        page_depotauszug_add = DepotauszugAdd(driver=driver)
        page_sparkonto_uebersicht = DepotUebersicht(driver=driver)

        page_depot_add.visit()
        page_depot_add.add('TestKonto')
        page_depotwert_add.visit()
        page_depotwert_add.add('Testdepotwert', 'ISINDEMO')
        page_order_add.visit()
        page_order_add.add('2020-01-01', 'testname', 'Testdepotwert (ISINDEMO)', 'Testdepot', 10,  True)
        page_depotauszug_add.visit()
        page_depotauszug_add.add('2020-01-02', 'TestKonto', 'ISINDEMO', 9)

        page_sparkonto_uebersicht.visit()

        assert page_sparkonto_uebersicht.get(0) == {
            'name': 'TestKonto',
            'typ': 'Depot',
            'wert': '9,00',
            'aufbuchungen': '10,00',
            'difference': '-1,00'
        }
        close_driver(driver)

    def teste_uebersicht_depotwerte(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_depotwert_add = DepotwertAdd(driver=driver)
        page_depotwert_uebersicht = DepotwertUebersicht(driver=driver)

        page_depotwert_add.visit()
        page_depotwert_add.add('Testdepotwert', 'ISINDEMO')

        page_depotwert_uebersicht.visit()

        assert page_depotwert_uebersicht.get(0) == {
            'name': 'Testdepotwert',
            'isin': 'ISINDEMO',
            'wert': '0,00'
        }
        close_driver(driver)



