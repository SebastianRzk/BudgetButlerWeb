import pytest
from selenium import webdriver
import os
from selenium.webdriver.support.select import Select

class SeleniumTestClass:

    def _to_param(self, name, provider):
        return pytest.param(provider, id=name)

    def pytest_generate_tests(self, metafunc):
        if 'TRAVIS_INTEGRATION' in os.environ:
            drivers = [self._to_param('PhantomJS', webdriver.PhantomJS)]
        else:
            drivers = [self._to_param('Chrome', webdriver.Chrome)]

        metafunc.parametrize(argnames='driver_provider', argvalues=drivers, scope="module")



def enter_test_mode(driver):
    driver.get('http://localhost:8000/production/testmode')


def fill_element(driver, elementname, content):
    elem = driver.find_element_by_name(elementname)
    elem.clear()
    elem.send_keys(content)

def define_kategorie(driver, kategorie_name):
    driver.get('http://127.0.0.1:8000/configuration/')
    fill_element(driver, 'neue_kategorie', kategorie_name)
    button = driver.find_element_by_id('add_kategorie')
    button.click()

def select_option(driver, option_id, item):
    el = driver.find_element_by_id(option_id)
    for option in el.find_elements_by_tag_name('option'):
        if option.text == item:
            option.click()  # select() in earlier versions of webdriver
            break

def get_selected_option(driver, option_id):
    select = Select(driver.find_element_by_id(option_id))
    selected_option = select.first_selected_option
    return selected_option.text




