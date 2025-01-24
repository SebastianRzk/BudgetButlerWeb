from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import shutil


def content_of(driver, element_id):
    return driver.find_element(By.ID, element_id).get_attribute('innerHTML')


def enter_test_mode(driver):
    shutil.copyfile('./Database_Test_User.csv.backup', '../data/Database_Test_User.csv')
    driver.get('http://localhost:5000/reload_database/')


def fill_element(driver, elementname, content):
    elem = driver.find_element(By.NAME, elementname)
    elem.clear()
    elem.send_keys(content)


def select_option(driver, option_id, item):
    el = driver.find_element(By.ID, option_id)
    for option in el.find_elements(By.TAG_NAME, 'option'):
        if option.text == item:
            option.click()
            break


def click_add_button(driver, button_postfix = ''):
    add_button = driver.find_element(By.ID, 'add' + button_postfix)
    add_button.click()


def fill_element_by_id(driver, elementname, content):
    elem = driver.find_element(By.ID, elementname)
    elem.clear()
    elem.send_keys(content)


def define_kategorie(driver, kategorie_name):
    driver.get('http://127.0.0.1:5000/configuration/')
    fill_element(driver, 'neue_kategorie', kategorie_name)
    button = driver.find_element(By.ID, 'add_kategorie')
    button.click()


def get_options(driver, option_id):
    el = driver.find_element(By.ID, option_id)
    result = []
    for option in el.find_elements(By.TAG_NAME, 'option'):
        result.append(option.text)
    return result


def get_selected_option(driver, option_id):
    select = Select(driver.find_element(By.ID, option_id))
    selected_option = select.first_selected_option
    return selected_option.text


def pagename(driver):
    return content_of(driver, 'pagetitle')
