from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select



def test_add_ausgabe(driver):
    driver.get('http://localhost:8000/addeinzelbuchung/')
    fill_element(driver, 'date', '17031994')
    fill_element(driver, 'name', 'eine ausgabe')
    fill_element(driver, 'wert', '12,34')



def enter_test_mode(driver):
    driver.get('http://localhost:8000/production/testmode')

def test_define_kategorie(driver):
    driver.get('http://127.0.0.1:8000/configuration/')
    kategorie_name = 'testkategorie'
    fill_element(driver, 'neue_kategorie', kategorie_name)
    button = driver.find_element_by_id('add_kategorie')
    button.click()

    _look_for_kategorie_in_auswahl(driver, kategorie_name, 'http://localhost:8000/addeinzelbuchung/')
    _look_for_kategorie_in_auswahl(driver, kategorie_name, 'http://localhost:8000/addeinnahme/')
    _look_for_kategorie_in_auswahl(driver, kategorie_name, 'http://localhost:8000/adddauerauftrag/')

def _look_for_kategorie_in_auswahl(driver, kategorie_name , link):
    driver.get(link)
    kategorie_auswahl = Select(driver.find_element_by_id('kategorie_auswahl'))

    print(kategorie_auswahl.options)
    assert kategorie_name in map(lambda x: x.text, kategorie_auswahl.options)


def fill_element(driver, elementname, content):
    elem = driver.find_element_by_name(elementname)
    elem.clear()
    elem.send_keys(content)








if __name__ == "__main__":
    DRIVER = webdriver.Chrome()
    enter_test_mode(DRIVER)

    test_define_kategorie(DRIVER)

    test_add_ausgabe(DRIVER)

    time.sleep(20)
    DRIVER.close()