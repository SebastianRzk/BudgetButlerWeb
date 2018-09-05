from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element

class TestLogin(SeleniumTestClass):
    def test_login_page(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/login.php')
        assert driver.title == 'BudgetButlerWeb - Login'
        close_driver(driver)

    def test_login_admin(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/login.php')

        fill_element(driver, 'email', 'admin@admin.de')
        fill_element(driver, 'password', 'admin')
        driver.find_element_by_id('btn_login').click()
        assert driver.title == 'BudgetButlerWeb - Dashboard'
        driver.get('http://localhost/logout.php')
        assert driver.title == 'BudgetButlerWeb - Logout'
        close_driver(driver)