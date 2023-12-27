import pytest
from selenium import webdriver
import os
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from butler_offline_selenium_tests import selenium_test

BROWSER_CACHE = []
BROWSER_INSTANCES = []


class SeleniumTestClass:

    def _to_param(self, name, provider, closer):
        return pytest.param(provider, closer, id=name)

    def pytest_generate_tests(self, metafunc):
        if 'INTEGRATION_TESTS' in os.environ:
            firefox = [self._to_param('Firefox headless', _launch_headless_firefox, close_driver)]
        else:
            firefox = [self._to_param('Firefox', _launch_head_firefox, close_driver)]

        metafunc.parametrize(argnames=['get_driver', 'close_driver'], argvalues=firefox, scope="module")


def close_driver(driver):
    if driver in selenium_test.BROWSER_INSTANCES:
        selenium_test.BROWSER_INSTANCES.remove(driver)

    if 'INTEGRATION_TESTS' in os.environ:
        selenium_test.BROWSER_CACHE.append(driver)
        return
    driver.close()


def _launch_head_firefox(window_size_x: int = 1920, window_size_y: int = 1080):
    firefox_options = Options()
    firefox_options.add_argument(f'--window-size={window_size_x},{window_size_y}')
    firefox_options.add_argument(f'--width={window_size_y}')
    firefox_options.add_argument(f'--height={window_size_x}')
    return webdriver.Firefox(options=firefox_options)


def _launch_headless_firefox():
    if selenium_test.BROWSER_CACHE:
        browser = selenium_test.BROWSER_CACHE[0]
        selenium_test.BROWSER_CACHE.remove(browser)
        selenium_test.BROWSER_INSTANCES.append(browser)
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
    selenium_test.BROWSER_INSTANCES.append(browser)
    return browser
