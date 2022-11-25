import pytest
from selenium import webdriver
import os
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from butler_offline_selenium_tests import SeleniumTest

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




