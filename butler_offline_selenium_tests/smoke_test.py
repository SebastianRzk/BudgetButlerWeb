from selenium.webdriver.common.by import By

from butler_offline_selenium_tests.selenium_test import SeleniumTestClass


class TestHeadlines(SeleniumTestClass):
    def test_add_dauerauftrag(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/adddauerauftrag/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Dauerauftrag hinzufügen'
        close_driver(driver)

    def test_add_einnahme(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/addeinnahme/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Einnahme hinzufügen'
        close_driver(driver)

    def test_add_ausgabe(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/addausgabe/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Ausgabe hinzufügen'
        close_driver(driver)

    def test_add_gemeinsam(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/addgemeinsam/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Neue gemeinsame Ausgabe'
        close_driver(driver)

    def test_configuration(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/configuration/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Einstellungen'
        close_driver(driver)

    def test_dashboard(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht'
        close_driver(driver)

    def test_dauerauftragsuebersicht(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/dauerauftraguebersicht/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht Daueraufträge'
        close_driver(driver)

    def test_einzelbuchungsuebersicht(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/uebersicht/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht Einzelbuchungen'
        close_driver(driver)

    def test_gemeinsam_abrechnen(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/gemeinsamabrechnen/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Gemeinsam abrechnen'
        close_driver(driver)

    def test_gemeinsam_uebersicht(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/gemeinsameuebersicht/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht Buchungen'
        close_driver(driver)

    def test_importd(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/import/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Export / Import'
        close_driver(driver)

    def test_jahresuebersicht(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/jahresuebersicht/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Jahresübersicht'
        close_driver(driver)

    def test_monatsuebersicht(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/monatsuebersicht/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Monatsübersicht'
        close_driver(driver)

    def test_uebesicht_abrechnungen(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/uebersichtabrechnungen/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht Abrechnungen'
        close_driver(driver)

    def test_add_sparbuchung(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/add_sparbuchung/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Neue Sparbuchung'
        close_driver(driver)

    def test_add_sparkonto(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/add_sparkonto/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Neues Sparkonto'
        close_driver(driver)

    def test_add_depotwert(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/add_depotwert/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Neuer Depotwert'
        close_driver(driver)

    def test_add_depotauszug(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/add_depotauszug/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Neuer Depotauszug'
        close_driver(driver)

    def test_uebersicht_depotauszuege(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/uebersicht_depotauszuege/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht Depotauszüge'
        close_driver(driver)

    def test_add_order(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/add_order/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Neue Order'
        close_driver(driver)

    def test_uebesicht_sparbuchungen(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/uebersicht_sparbuchungen/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht Sparbuchungen'
        close_driver(driver)

    def test_uebesicht_sparkontos(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/uebersicht_sparkontos/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht Sparkontos'
        close_driver(driver)

    def test_uebesicht_depotwerte(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/uebersicht_depotwerte/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht Depotwerte'
        close_driver(driver)

    def test_uebesicht_order(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/uebersicht_order/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht Order'
        close_driver(driver)

    def test_add_orderdauerauftrag(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/add_orderdauerauftrag/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Neuer Order-Dauerauftrag'
        close_driver(driver)

    def test_uebesicht_orderdauerauftrag(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/uebersicht_orderdauerauftrag/')
        assert driver.find_element(By.ID, 'pagetitle').get_attribute('innerHTML') == 'Übersicht Order-Daueraufträge'
        close_driver(driver)
