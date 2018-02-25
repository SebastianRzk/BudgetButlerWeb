import pytest
from selenium import webdriver
import os
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import SeleniumTest

CHROME_CACHE = []
CHROME_INSTANCES = []

class SeleniumTestClass:

    def _to_param(self, name, provider, closer):
        return pytest.param(provider, closer, id=name)

    def pytest_generate_tests(self, metafunc):
        if 'TRAVIS_INTEGRATION' in os.environ:
            chrome = [self._to_param('Chromium  headless', _launch_headles_chromium, close_driver)]
        else:
            chrome = [self._to_param('Chromium', _launch_head_chrome, close_driver)]

        metafunc.parametrize(argnames=['get_driver', 'close_driver'], argvalues=chrome, scope="module")

def close_driver(driver):
    if driver in SeleniumTest.CHROME_INSTANCES:
        SeleniumTest.CHROME_INSTANCES.remove(driver)

    if 'TRAVIS_INTEGRATION' in os.environ:
        SeleniumTest.CHROME_CACHE.append(driver)
        return
    driver.close()

def _launch_head_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(chrome_options=chrome_options)

def _launch_headles_chromium():
    if SeleniumTest.CHROME_CACHE:
        browser = SeleniumTest.CHROME_CACHE[0]
        SeleniumTest.CHROME_CACHE.remove(browser)
        SeleniumTest.CHROME_INSTANCES.append(browser)
        return browser

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)
    SeleniumTest.CHROME_INSTANCES.append(browser)
    return browser

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

def get_options(driver, option_id):
    el = driver.find_element_by_id(option_id)
    result = []
    for option in el.find_elements_by_tag_name('option'):
        result.append(option.text)
    return result

def get_selected_option(driver, option_id):
    select = Select(driver.find_element_by_id(option_id))
    selected_option = select.first_selected_option
    return selected_option.text




