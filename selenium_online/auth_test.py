from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import login
from SeleniumTest import generate_unique_name
from selenium.webdriver.common.keys import Keys

class TestLogin(SeleniumTestClass):
    def test_login_page(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/login.php')
        assert driver.title == 'BudgetButlerWeb - Login'
        close_driver(driver)

    def test_login_admin(self, get_driver, close_driver):
        driver = get_driver()

        login(driver, 'admin@admin.de', 'admin')
        driver.get('http://localhost/logout.php')
        assert driver.title == 'BudgetButlerWeb - Logout'
        close_driver(driver)


    def test_add_user(self, get_driver, close_driver):
        driver = get_driver()

        new_user_id = generate_unique_name()
        new_user_email = new_user_id + '@sebastian.de'
        passwd = 'funnypass'

        login(driver, 'admin@admin.de', 'admin')

        driver.get('http://localhost/dashboard.php')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        fill_element(driver, 'username', new_user_id)
        fill_element(driver, 'email', new_user_email)
        fill_element(driver, 'password', passwd)
        driver.find_element_by_id('btn_add_user').send_keys(Keys.ENTER)

        driver.get('http://localhost/logout.php')

        login(driver, new_user_email, passwd)
        assert driver.title == 'BudgetButlerWeb - Dashboard'
        driver.get('http://localhost/logout.php')
        assert driver.title == 'BudgetButlerWeb - Logout'
        close_driver(driver)