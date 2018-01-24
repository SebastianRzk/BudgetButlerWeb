'''
Created on 23.11.2017

@author: sebastian
'''
from SeleniumTest import SeleniumTestClass
from SeleniumTest import enter_test_mode
from SeleniumTest import get_options
from SeleniumTest import fill_element

class TestUI(SeleniumTestClass):
    def teste_change_partnername(self, driver_provider):
        driver = driver_provider()
        enter_test_mode(driver)
        driver.get('http://localhost:8000/addgemeinsam/')
        assert set(get_options(driver, 'person_auswahl')) == set(['test', 'Maureen'])

        driver.get('http://localhost:8000/configuration/')
        fill_element(driver, 'partnername', 'Olaf')
        driver.find_element_by_id('set_partnername').click()

        driver.get('http://localhost:8000/addgemeinsam/')
        assert set(get_options(driver, 'person_auswahl')) == set(['test', 'Olaf'])
        driver.close()
        
