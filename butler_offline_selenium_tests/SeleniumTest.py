import pytest
from selenium import webdriver
import os
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import SeleniumTest

CHROME_CACHE = []
CHROME_INSTANCES = []

class SeleniumTestClass:

    def _to_param(self, name, provider, closer):
        return pytest.param(provider, closer, id=name)

    def pytest_generate_tests(self, metafunc):
        if 'TRAVIS_INTEGRATION' in os.environ:
            chrome = [self._to_param('Firefox headless', _launch_headles_firefox, close_driver)]
        else:
            chrome = [self._to_param('Firefox', _launch_head_firefox, close_driver)]

        metafunc.parametrize(argnames=['get_driver', 'close_driver'], argvalues=chrome, scope="module")

def close_driver(driver):
    if driver in SeleniumTest.CHROME_INSTANCES:
        SeleniumTest.CHROME_INSTANCES.remove(driver)

    if 'TRAVIS_INTEGRATION' in os.environ:
        SeleniumTest.CHROME_CACHE.append(driver)
        return
    driver.close()

def content_of(driver, element_id):
    return driver.find_element_by_id(element_id).get_attribute('innerHTML')


def _launch_head_firefox():
    firefox_options = Options()
    firefox_options.add_argument("--window-size=1920,1080")
    return webdriver.Firefox(options=firefox_options)

def _launch_headles_firefox():
    if SeleniumTest.CHROME_CACHE:
        browser = SeleniumTest.CHROME_CACHE[0]
        SeleniumTest.CHROME_CACHE.remove(browser)
        SeleniumTest.CHROME_INSTANCES.append(browser)
        return browser

    firefox_options = Options()
    firefox_options.add_argument("-headless")
    firefox_options.add_argument("--window-size=1920,1080")

    profile = FirefoxProfile()
    profile.set_preference('browser.cache.disk.enable', False)
    profile.set_preference('browser.cache.memory.enable', False)
    profile.set_preference('browser.cache.offline.enable', False)
    profile.set_preference('network.cookie.cookieBehavior', 2)

    browser = webdriver.Firefox(options=firefox_options, firefox_profile=profile)
    SeleniumTest.CHROME_INSTANCES.append(browser)
    return browser

def enter_test_mode(driver):
    driver.get('http://localhost:5000/production/testmode')


def fill_element(driver, elementname, content):
    elem = driver.find_element_by_name(elementname)
    elem.clear()
    elem.send_keys(content)

def select_option(driver, option_id, item):
    el = driver.find_element_by_id(option_id)
    for option in el.find_elements_by_tag_name('option'):
        if option.text == item:
            option.click()  # select() in earlier versions of webdriver
            break


def fill_element_by_id(driver, elementname, content):
    elem = driver.find_element_by_id(elementname)
    elem.clear()
    elem.send_keys(content)

def define_kategorie(driver, kategorie_name):
    driver.get('http://127.0.0.1:5000/configuration/')
    fill_element(driver, 'neue_kategorie', kategorie_name)
    button = driver.find_element_by_id('add_kategorie')
    button.click()

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

def pagename(driver):
    return content_of(driver, 'pagetitle')




