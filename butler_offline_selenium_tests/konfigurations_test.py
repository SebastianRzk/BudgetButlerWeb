from butler_offline_selenium_tests.selenium_test import SeleniumTestClass
from butler_offline_selenium_tests.page.util import enter_test_mode
from butler_offline_selenium_tests.page.gemeinsam.gemeinsam_add import GemeinsamAdd
from butler_offline_selenium_tests.page.core.configuration import Configuration
from butler_offline_selenium_tests.page.core.menu import Menu
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchung_add import EinzelbuchungAdd
from butler_offline_selenium_tests.page.einzelbuchungen.dauerauftrag_add import DauerauftragAdd
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchungen_uebersicht import EinzelbuchungenUebersicht
from butler_offline_selenium_tests.page.einzelbuchungen.dauerautrag_uebersicht import DauerauftragUebersicht


class TestUI(SeleniumTestClass):

    def teste_change_partnername(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_configuration = Configuration(driver=driver)

        page_gemeinsam_add.visit()
        assert page_gemeinsam_add.partner_options() == {'test', 'Partner'}

        page_configuration.visit()
        page_configuration.update_partnername('Olaf')

        page_gemeinsam_add.visit()
        assert page_gemeinsam_add.partner_options() == {'test', 'Olaf'}
        close_driver(driver)

    def test_change_database(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_gemeinsam_add = GemeinsamAdd(driver=driver)
        page_menu = Menu(driver=driver)

        page_gemeinsam_add.visit()
        assert page_gemeinsam_add.partner_options() == {'test', 'Partner'}

        page_menu.change_database('test')
        assert page_menu.get_title() == '~~~test~~~'

        page_menu.change_database('Partner')
        assert page_menu.get_title() == '~~~Partner~~~'
        close_driver(driver)

    def teste_theme_color(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_einzelbuchungen_add = EinzelbuchungAdd(driver=driver)
        page_configuration = Configuration(driver=driver)

        page_einzelbuchungen_add.visit()
        assert page_einzelbuchungen_add.add_button_color() == 'rgb(0, 172, 214)'

        page_configuration.visit()
        page_configuration.update_theme_color('#000000')

        page_einzelbuchungen_add.visit()
        assert page_einzelbuchungen_add.add_button_color() == 'rgb(0, 0, 0)'

        close_driver(driver)

    def test_create_backup(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_configuration = Configuration(driver=driver)
        page_configuration.visit()
        page_configuration.click_on_backup()

        assert page_configuration.get_page_message() == 'Backup erstellt'

        close_driver(driver)

    def test_rename_kategorie(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)

        page_einzelbuchungen_add = EinzelbuchungAdd(driver=driver)
        page_dauerauftrag_add = DauerauftragAdd(driver=driver)
        page_configuration = Configuration(driver=driver)
        page_einzelbuchungen = EinzelbuchungenUebersicht(driver=driver)
        page_dauerauftraege = DauerauftragUebersicht(driver=driver)

        page_einzelbuchungen_add.visit()
        page_einzelbuchungen_add.define_kategorie('kategorie_to_rename')
        page_einzelbuchungen_add.add(
            kategorie='kategorie_to_rename',
            name='name',
            wert=1,
            date='2022-01-01'
        )

        page_dauerauftrag_add.visit()
        page_dauerauftrag_add.add(
            kategorie='kategorie_to_rename',
            wert=1,
            name='name',
            endedatum='2022-01-01',
            startdatum='2021-01-01',
            typ='Ausgabe'
        )

        page_configuration.visit()
        page_configuration.rename(
            kategorie_neu='kategorie_renamed',
            kategorie_alt='kategorie_to_rename'
        )

        assert page_configuration.get_page_message() == ('Kategorie kategorie_to_rename erfolgreich in '
                                                         'kategorie_renamed umbenannt. <br> '
                                                         '1 Einzelbuchungen wurden aktualisiert <br> '
                                                         '1 Daueraufträge wurden aktualisiert')

        page_einzelbuchungen.visit()
        page_einzelbuchungen.open_module(month='1', year='2022')
        assert page_einzelbuchungen.get_item_in_opened_module(12)['kategorie'] == 'kategorie_renamed'

        page_dauerauftraege.visit()
        assert page_dauerauftraege.get_row(0)['kategorie'] == 'kategorie_renamed'

        close_driver(driver)
