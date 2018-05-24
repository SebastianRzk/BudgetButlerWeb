'''
Created on 23.11.2017

@author: sebastian
'''
from SeleniumTest import SeleniumTestClass
from SeleniumTest import enter_test_mode
from SeleniumTest import get_options
from SeleniumTest import fill_element


class TestUI(SeleniumTestClass):

    def teste_change_partnername(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        driver.get('http://localhost:8000/addgemeinsam/')
        assert set(get_options(driver, 'person_auswahl')) == set(['test', 'Maureen'])

        driver.get('http://localhost:8000/configuration/')
        fill_element(driver, 'partnername', 'Olaf')
        driver.find_element_by_id('set_partnername').click()

        driver.get('http://localhost:8000/addgemeinsam/')
        assert set(get_options(driver, 'person_auswahl')) == set(['test', 'Olaf'])
        close_driver(driver)

    def teste_theme_color(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        driver.get('http://127.0.0.1:8000/addeinzelbuchung/')
        add_button = driver.find_element_by_id('add')
        color_before = add_button.value_of_css_property("background-color")
        assert color_before == 'rgba(0, 172, 214, 1)'

        driver.get('http://127.0.0.1:8000/configuration/')
        driver.execute_script("document.getElementById('themecolor').setAttribute('value', '#000000')")
        driver.find_element_by_id('change_themecolor').click()

        driver.get('http://127.0.0.1:8000/addeinzelbuchung/')
        add_button = driver.find_element_by_id('add')
        color_before = add_button.value_of_css_property("background-color")
        assert color_before == 'rgba(0, 0, 0, 1)'

        close_driver(driver)

