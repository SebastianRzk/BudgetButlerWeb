from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import enter_test_mode
from butler_offline_selenium_tests.page.sparen.depot_add import DepotAdd
from butler_offline_selenium_tests.page.sparen.depotwert_add import DepotwertAdd
from butler_offline_selenium_tests.page.sparen.order_add import OrderAdd
from butler_offline_selenium_tests.page.sparen.depotauszug_add import DepotauszugAdd
from butler_offline_selenium_tests.page.sparen.orderdauerauftrag_add import OrderDauerauftragAdd
from butler_offline_selenium_tests.page.sparen.order_uebersicht import OrderUebersicht
from butler_offline_selenium_tests.page.sparen.depot_uebersicht import DepotUebersicht


class TestUI(SeleniumTestClass):


    def teste_uebersicht_kontos(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_depot_add = DepotAdd(driver=driver)
        page_depotwert_add = DepotwertAdd(driver=driver)
        page_order_add = OrderAdd(driver=driver)
        page_depotauszug_add = DepotauszugAdd(driver=driver)
        page_sparkonto_uebersicht = DepotUebersicht(driver=driver)

        page_depot_add.visit()
        page_depot_add.add('TestDepot')

        page_depotwert_add.visit()
        page_depotwert_add.add('Depotwert1', 'Isin1')

        page_order_add.visit()
        page_order_add.add('2020-01-01', 'first order', 'Isin1', 'TestDepot', 123, True)

        page_depotauszug_add.visit()
        page_depotauszug_add.add('2020-01-01', 'TestDepot', 'Isin1', 124)

        page_sparkonto_uebersicht.visit()

        assert page_sparkonto_uebersicht.get(0) == {
            'name': 'TestDepot',
            'typ': 'Depot',
            'wert': '124,00',
            'aufbuchungen': '123,00',
            'difference': '1,00'
        }

        assert page_sparkonto_uebersicht.get_gesamt() == {
            'wert': '124,00',
            'aufbuchungen': '123,00',
            'difference': '1,00'
        }
        close_driver(driver)


    def teste_orderdauerauftrag(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_depot_add = DepotAdd(driver=driver)
        page_depotwert_add = DepotwertAdd(driver=driver)
        page_sparkonto_uebersicht = DepotUebersicht(driver=driver)
        page_orderdauerauftrag_add = OrderDauerauftragAdd(driver=driver)
        page_order_uebersicht = OrderUebersicht(driver=driver)

        page_depot_add.visit()
        page_depot_add.add('TestDepot')

        page_depotwert_add.visit()
        page_depotwert_add.add('Depotwert1', 'Isin1')

        page_orderdauerauftrag_add.visit()
        page_orderdauerauftrag_add.add('2020-01-01', '2020-02-02', 'first order', 'Isin1', 'TestDepot', 101, True)

        page_sparkonto_uebersicht.visit()

        assert page_sparkonto_uebersicht.get(0)['aufbuchungen'] == '202,00'

        page_order_uebersicht.visit()

        assert page_order_uebersicht.get(0) == {
            'datum': '01.01.2020',
            'konto': 'TestDepot',
            'depotwert': 'Depotwert1 (Isin1)',
            'name': 'first order',
            'wert': '101,00'
        }

        assert page_order_uebersicht.get(1) == {
            'datum': '01.02.2020',
            'konto': 'TestDepot',
            'depotwert': 'Depotwert1 (Isin1)',
            'name': 'first order',
            'wert': '101,00'
        }

        close_driver(driver)



