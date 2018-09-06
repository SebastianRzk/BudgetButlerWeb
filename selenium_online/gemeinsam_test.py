from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import login
from SeleniumTest import generate_unique_name
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class TestGemeinsam(SeleniumTestClass):
    def test_add_and_delete_connection(self, get_driver, close_driver):
        driver = get_driver()

        user1 = generate_unique_name() + '1'
        user1passwd = 'u1pass'
        user2 = generate_unique_name() + '2'
        user2passwd = 'u2pass'

        # Create user
        self.create_user(driver, user1, user1passwd)
        self.create_user(driver, user2, user2passwd)

        # Create connnection from user1 to user2. Status should be PENDING
        login(driver, user1 + '@s.de', user1passwd)
        fill_element(driver, 'other_person', user2)
        driver.find_element_by_id('add_other_person').send_keys(Keys.ENTER)
        status = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'gemeinschaftsstatus')))
        assert status.get_attribute('innerHTML') == 'Warten auf Partner.'
        driver.get('http://localhost/logout.php')

        # Create connection from user2 to user1, Status should be ACTIVE
        login(driver, user2 + '@s.de', user2passwd)
        fill_element(driver, 'other_person', user1)
        driver.find_element_by_id('add_other_person').send_keys(Keys.ENTER)
        status = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'gemeinschaftsstatus')))
        assert status.get_attribute('innerHTML') == 'Gemeinsschaft bestätigt. Gemeinsame Buchungen aktiv.'
        driver.get('http://localhost/logout.php')
        login(driver, user1 + '@s.de', user1passwd)
        status = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'gemeinschaftsstatus')))
        assert status.get_attribute('innerHTML') == 'Gemeinsschaft bestätigt. Gemeinsame Buchungen aktiv.'

        # Delete connection, status sould be pending
        driver.find_element_by_id('btn_delete_other').send_keys(Keys.ENTER)
        status = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'add_other_person')))
        driver.get('http://localhost/logout.php')
        login(driver, user2 + '@s.de', user2passwd)
        status = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'gemeinschaftsstatus')))
        assert status.get_attribute('innerHTML') == 'Warten auf Partner.'
        driver.get('http://localhost/logout.php')

        close_driver(driver)


    def create_user(self, driver, new_user_id, passwd):
        new_user_email = new_user_id + '@s.de'

        login(driver, 'admin@admin.de', 'admin')

        driver.get('http://localhost/dashboard.php')
        fill_element(driver, 'username', new_user_id)
        fill_element(driver, 'email', new_user_email)
        fill_element(driver, 'password', passwd)
        driver.find_element_by_id('btn_add_user').send_keys(Keys.ENTER)

        driver.get('http://localhost/logout.php')

        login(driver, new_user_email, passwd)
        assert driver.title == 'BudgetButlerWeb - Dashboard'
        driver.get('http://localhost/logout.php')
        assert driver.title == 'BudgetButlerWeb - Logout'