'''

'''

from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import fill_element_by_id
from SeleniumTest import enter_test_mode
from SeleniumTest import define_kategorie
from SeleniumTest import select_option
from SeleniumTest import content_of

class TestGemeinsameAbrechnung(SeleniumTestClass):
    test_change_veraeltnis_abrechnung = '''
			Abrechnung vom 22.01.2019 (01.01.2010-01.01.2010)
########################################
 Ergebnis:
test übernimmt einen Anteil von 70% der Ausgaben.

Maureen bekommt von test noch 70.00€.

Ausgaben von Maureen          -100.00
Ausgaben von test                0.00
--------------------------------------
Gesamt                        -100.00


########################################
 Ausgaben von Maureen
########################################
 Datum      Kategorie    Name                    Wert
01.01.2010  0test_kategorie 0name                -100.00


########################################
 Ausgaben von test
########################################
 Datum      Kategorie    Name                    Wert


#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2010-01-01,0test_kategorie,0name,-30.00,False
#######MaschinenimportEnd

		'''

    def test_change_verhaeltnis(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_ausgabe(driver, '2010-01-01', '0name', '0test_kategorie', '100', 'Maureen')

        driver.get('http://localhost:5000/gemeinsamabrechnen/')

        assert content_of(driver, 'ausgabe_sebastian') == "0.00"
        assert content_of(driver, 'ausgabe_sebastian_soll') == "50.00"
        assert content_of(driver, 'ausgabe_sebastian_diff') == "-50.00"

        assert content_of(driver, 'ausgabe_maureen') == "100.00"
        assert content_of(driver, 'ausgabe_maureen_soll') == "50.00"
        assert content_of(driver, 'ausgabe_maureen_diff') == "50.00"

        fill_element_by_id(driver, 'abrechnungsverhaeltnis', '70')
        driver.find_element_by_id('abrechnung_aktualisieren').click()

        assert content_of(driver, 'ausgabe_sebastian') == "0.00"
        assert content_of(driver, 'ausgabe_sebastian_soll') == "70.00"
        assert content_of(driver, 'ausgabe_sebastian_diff') == "-70.00"

        assert content_of(driver, 'ausgabe_maureen') == "100.00"
        assert content_of(driver, 'ausgabe_maureen_soll') == "30.00"
        assert content_of(driver, 'ausgabe_maureen_diff') == "70.00"

        driver.find_element_by_id('abrechnen').click()
        print('[',content_of(driver, 'abrechnung').replace('<br>', '\n'),']')
        assert content_of(driver, 'abrechnung').replace('<br>', '\n') == self.test_change_veraeltnis_abrechnung
        close_driver(driver)

    set_limit_abrechnung = '''
			Abrechnung vom 22.01.2019 (01.01.2010-01.01.2010)
########################################
 Ergebnis:
Durch das Limit bei test von 30 EUR wurde das Verhältnis von 50 auf 30.0 aktualisiert

Maureen bekommt von test noch 30.00€.

Ausgaben von Maureen          -100.00
Ausgaben von test                0.00
--------------------------------------
Gesamt                        -100.00


########################################
 Ausgaben von Maureen
########################################
 Datum      Kategorie    Name                    Wert
01.01.2010  0test_kategorie 0name                -100.00


########################################
 Ausgaben von test
########################################
 Datum      Kategorie    Name                    Wert


#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2010-01-01,0test_kategorie,0name,-70.00,False
#######MaschinenimportEnd

		'''

    def test_set_limit(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')
        self._add_ausgabe(driver, '2010-01-01', '0name', '0test_kategorie', '100', 'Maureen')

        driver.get('http://localhost:5000/gemeinsamabrechnen/')

        assert content_of(driver, 'ausgabe_sebastian') == "0.00"
        assert content_of(driver, 'ausgabe_sebastian_soll') == "50.00"
        assert content_of(driver, 'ausgabe_sebastian_diff') == "-50.00"

        assert content_of(driver, 'ausgabe_maureen') == "100.00"
        assert content_of(driver, 'ausgabe_maureen_soll') == "50.00"
        assert content_of(driver, 'ausgabe_maureen_diff') == "50.00"

        driver.find_element_by_id('set_limit').click()
        select_option(driver, 'set_limit_fuer', 'test')
        fill_element(driver, 'set_limit_value', '30')
        driver.find_element_by_id('abrechnung_aktualisieren').click()

        assert content_of(driver, 'ausgabe_sebastian') == "0.00"
        assert content_of(driver, 'ausgabe_sebastian_soll') == "30.00"
        assert content_of(driver, 'ausgabe_sebastian_diff') == "-30.00"

        assert content_of(driver, 'ausgabe_maureen') == "100.00"
        assert content_of(driver, 'ausgabe_maureen_soll') == "70.00"
        assert content_of(driver, 'ausgabe_maureen_diff') == "30.00"

        driver.find_element_by_id('abrechnen').click()
        print('[',content_of(driver, 'abrechnung').replace('<br>', '\n'),']')
        assert content_of(driver, 'abrechnung').replace('<br>', '\n') == self.set_limit_abrechnung
        close_driver(driver)

    set_limit_abrechnung_ausgleich = '''
			Abrechnung vom 22.01.2019 (01.01.2010-01.01.2010)
########################################
 Ergebnis:
Durch das Limit bei test von 30 EUR wurde das Verhältnis von 50 auf 30.0 aktualisiert

Maureen bekommt von test noch 30.00€.

Ausgaben von Maureen          -100.00
Ausgaben von test                0.00
--------------------------------------
Gesamt                        -100.00


########################################
 Ausgaben von Maureen
########################################
 Datum      Kategorie    Name                    Wert
01.01.2010  0test_kategorie 0name                -100.00


########################################
 Ausgaben von test
########################################
 Datum      Kategorie    Name                    Wert


#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2010-01-01,0test_kategorie,0name,-50.00,False
2010-01-01,test ausgleich,test ausgleich,-20.00,False
#######MaschinenimportEnd

		'''

    def test_set_limit_and_add_ausgleichsbuchungen_both(self, get_driver, close_driver):
        driver = get_driver()
        enter_test_mode(driver)
        define_kategorie(driver, '0test_kategorie')

        self._add_ausgabe(driver, '2010-01-01', '0name', '0test_kategorie', '100', 'Maureen')
        define_kategorie(driver, '1test_kategorie')

        driver.get('http://localhost:5000/gemeinsamabrechnen/')

        assert content_of(driver, 'ausgabe_sebastian') == "0.00"
        assert content_of(driver, 'ausgabe_sebastian_soll') == "50.00"
        assert content_of(driver, 'ausgabe_sebastian_diff') == "-50.00"

        assert content_of(driver, 'ausgabe_maureen') == "100.00"
        assert content_of(driver, 'ausgabe_maureen_soll') == "50.00"
        assert content_of(driver, 'ausgabe_maureen_diff') == "50.00"

        driver.find_element_by_id('set_limit').click()
        select_option(driver, 'set_limit_fuer', 'test')
        fill_element_by_id(driver, 'set_limit_value', '30')

        driver.find_element_by_id('set_self_kategorie').click()
        select_option(driver, 'set_self_kategorie_value', '1test_kategorie')

        driver.find_element_by_id('set_other_kategorie').click()
        fill_element_by_id(driver, 'set_other_kategorie_value', 'test ausgleich')

        driver.find_element_by_id('abrechnung_aktualisieren').click()

        assert content_of(driver, 'ausgabe_sebastian') == "0.00"
        assert content_of(driver, 'ausgabe_sebastian_soll') == "30.00"
        assert content_of(driver, 'ausgabe_sebastian_diff') == "-30.00"

        assert content_of(driver, 'ausgabe_maureen') == "100.00"
        assert content_of(driver, 'ausgabe_maureen_soll') == "70.00"
        assert content_of(driver, 'ausgabe_maureen_diff') == "30.00"

        driver.find_element_by_id('abrechnen').click()
        assert content_of(driver, 'abrechnung').replace('<br>', '\n') == self.set_limit_abrechnung_ausgleich

        driver.get('http://localhost:5000/uebersicht/')
        open_table_button = driver.find_element_by_id('open_2010.1')
        open_table_button.click()

        assert content_of(driver, 'item_0_id') == '0'
        assert content_of(driver, 'item_0_name') == '0name'
        assert content_of(driver, 'item_0_kategorie') == '0test_kategorie'
        assert content_of(driver, 'item_0_datum') == '01.01.2010'
        assert content_of(driver, 'item_0_wert') == '-50.00'

        assert content_of(driver, 'item_1_id') == '1'
        assert content_of(driver, 'item_1_name') == '1test_kategorie'
        assert content_of(driver, 'item_1_kategorie') == '1test_kategorie'
        assert content_of(driver, 'item_1_datum') == '01.01.2010'
        assert content_of(driver, 'item_1_wert') == '20.00'

        close_driver(driver)



    def _add_ausgabe(self, driver, date, name, kategorie, wert, person):
        driver.get('http://localhost:5000/addgemeinsam/')
        fill_element(driver, 'date', date)
        fill_element(driver, 'name', name)
        fill_element(driver, 'wert', wert)
        select_option(driver, 'kategorie_auswahl', kategorie)
        select_option(driver, 'person_auswahl', person)

        add_button = driver.find_element_by_id('add')
        add_button.click()