'''
Created on 23.11.2017

@author: sebastian
'''
from SeleniumTest import SeleniumTestClass
from time import sleep
from SeleniumTest import get_selected_option

class TestHeadlines(SeleniumTestClass):
    def test_add_dauerauftrag(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/adddauerauftrag/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Neuer Dauerauftrag'
        close_driver(driver)

    def test_add_einnahme(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/addeinnahme/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Neue Einnahme'
        close_driver(driver)

    def test_add_ausgabe(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/addausgabe/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Neue Ausgabe'
        close_driver(driver)

    def test_add_gemeinsam(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/addgemeinsam/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Neue gemeinsame Ausgabe'
        close_driver(driver)

    def test_configuration(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/configuration/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Einstellungen'
        close_driver(driver)

    def test_dashboard(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Übersicht'
        close_driver(driver)

    def test_dauerauftragsuebersicht(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/dauerauftraguebersicht/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Alle Daueraufträge'
        close_driver(driver)

    def test_gemeinsam_abrechnen(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/gemeinsamabrechnen/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Gemeinsam abrechnen'
        close_driver(driver)

    def test_gemeinsam_uebersicht(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/gemeinsameuebersicht/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Alle gem. Buchungen'
        close_driver(driver)

    def test_importd(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/import/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Export / Import'
        close_driver(driver)

    def test_jahresuebersicht(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/jahresuebersicht/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Jahresübersicht'
        close_driver(driver)

    def test_monatsuebersicht(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost:5000/monatsuebersicht/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Monatsübersicht'
        close_driver(driver)
