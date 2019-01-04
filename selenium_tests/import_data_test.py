'''
Created on 25.08.2018

@author: sebastian
'''
from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import enter_test_mode
from SeleniumTest import define_kategorie
from SeleniumTest import select_option
from SeleniumTest import get_selected_option
from SeleniumTest import pagename

class TestUI(SeleniumTestClass):

    _data = '''
#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-06,Essen,Edeka,-10.0,True
#######MaschinenimportEnd
            '''

    def teste_import_neue_kategorien(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        driver.get('http://localhost:5000/import/')
        fill_element(driver, 'import', self._data)
        driver.find_element_by_name('btn_import').click()

        assert pagename(driver) == 'Kategorien zuweisen'

        driver.find_element_by_name('action').click()

        driver.get('http://localhost:5000/uebersicht/')
        open_table_button = driver.find_element_by_id('open_2017.3')
        open_table_button.click()

        assert driver.find_element_by_id('item_0_id').get_attribute('innerHTML') == '0'
        assert driver.find_element_by_id('item_0_name').get_attribute('innerHTML') == 'Edeka'
        assert driver.find_element_by_id('item_0_kategorie').get_attribute('innerHTML') == 'Essen'
        assert driver.find_element_by_id('item_0_datum').get_attribute('innerHTML') == '06.03.2017'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '-10.00'

        close_driver(driver)

    def test_with_mapping_to_other_kategorie(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        define_kategorie(driver, 'nicht essen')
        driver.get('http://localhost:5000/import/')
        fill_element(driver, 'import', self._data)
        driver.find_element_by_name('btn_import').click()

        assert pagename(driver) == 'Kategorien zuweisen'

        select_option(driver, 'Essen_mapping', 'als nicht essen importieren')

        driver.find_element_by_name('action').click()

        driver.get('http://localhost:5000/uebersicht/')
        open_table_button = driver.find_element_by_id('open_2017.3')
        open_table_button.click()

        assert driver.find_element_by_id('item_0_id').get_attribute('innerHTML') == '0'
        assert driver.find_element_by_id('item_0_name').get_attribute('innerHTML') == 'Edeka'
        assert driver.find_element_by_id('item_0_kategorie').get_attribute('innerHTML') == 'nicht essen'
        assert driver.find_element_by_id('item_0_datum').get_attribute('innerHTML') == '06.03.2017'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '-10.00'

        close_driver(driver)


    def test_with_existing_kategorie(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        define_kategorie(driver, 'Essen')
        driver.get('http://localhost:5000/import/')
        fill_element(driver, 'import', self._data)
        driver.find_element_by_name('btn_import').click()

        assert pagename(driver) == 'Export / Import'

        driver.get('http://localhost:5000/uebersicht/')
        open_table_button = driver.find_element_by_id('open_2017.3')
        open_table_button.click()

        assert driver.find_element_by_id('item_0_id').get_attribute('innerHTML') == '0'
        assert driver.find_element_by_id('item_0_name').get_attribute('innerHTML') == 'Edeka'
        assert driver.find_element_by_id('item_0_kategorie').get_attribute('innerHTML') == 'Essen'
        assert driver.find_element_by_id('item_0_datum').get_attribute('innerHTML') == '06.03.2017'
        assert driver.find_element_by_id('item_0_wert').get_attribute('innerHTML') == '-10.00'

        close_driver(driver)

    def test_should_showSuccessMessage(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        define_kategorie(driver, 'Essen')
        driver.get('http://localhost:5000/import/')
        fill_element(driver, 'import', self._data)
        driver.find_element_by_name('btn_import').click()

        assert pagename(driver) == 'Export / Import'

        driver.get('http://localhost:5000/uebersicht/')
        open_table_button = driver.find_element_by_id('open_2017.3')
        open_table_button.click()

        assert driver.find_element_by_id('message-box-content').get_attribute('innerHTML') == '1 Buchung wurde importiert'
        close_driver(driver)









