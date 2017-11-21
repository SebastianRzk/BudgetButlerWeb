import pytest
from selenium import webdriver
import os

class SeleniumTestClass:

    def _to_param(self, name, provider):
        return pytest.param(provider, id=name)

    def pytest_generate_tests(self, metafunc):
        if 'TRAVIS_INTEGRATION' in os.environ:
            drivers = [lambda: webdriver.PhantomJS()]
        else:
            drivers = [lambda: webdriver.Chrome()]

        metafunc.parametrize(argnames='driver_provider', argvalues=drivers, scope="module")


