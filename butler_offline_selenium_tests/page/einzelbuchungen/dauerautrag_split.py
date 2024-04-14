from selenium.webdriver.common.by import By

from butler_offline_selenium_tests.page.util import fill_element


class DauerauftragSplit:
    def __init__(self, driver):
        self.driver = driver

    def get_vorgeschlagene_zeitstempel(self) -> list[str]:
        datums = self.driver.find_elements(by=By.NAME, value='datum-option')
        result = []
        for datum in datums:
            result.append(datum.get_attribute('innerHTML'))
        return result

    def setze_wert(self, neuer_wert) -> None:
        fill_element(self.driver, 'wert', neuer_wert)

    def waehle_zeitstempel_aus(self, zeitstempel: str) -> None:
        self.driver.find_element(by=By.ID, value='id_' + zeitstempel).click()

    def click_bestaetigen_button(self) -> None:
        go_button = self.driver.find_element(By.NAME, 'action')
        go_button.click()
