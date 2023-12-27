from time import sleep

from selenium.webdriver.common.by import By

from butler_offline.viewcore.converter import german_to_rfc as datum
from butler_offline_selenium_tests.page.einzelbuchungen.dauerauftrag_add import DauerauftragAdd
from butler_offline_selenium_tests.page.einzelbuchungen.einzelbuchung_add import EinzelbuchungAdd
from butler_offline_selenium_tests.page.gemeinsam.gemeinsam_abrechnen import GemeinsamAbrechnen
from butler_offline_selenium_tests.page.gemeinsam.gemeinsam_add import GemeinsamAdd
from butler_offline_selenium_tests.page.sparen.depot_add import DepotAdd
from butler_offline_selenium_tests.page.sparen.depotauszug_add import DepotauszugAdd
from butler_offline_selenium_tests.page.sparen.depotwert_add import DepotwertAdd
from butler_offline_selenium_tests.page.sparen.sparbuchung_add import SparbuchungAdd
from butler_offline_selenium_tests.page.sparen.order_add import OrderAdd
from butler_offline_selenium_tests.page.util import enter_test_mode
from butler_offline_selenium_tests.selenium_test import _launch_head_firefox, close_driver

driver = _launch_head_firefox(window_size_y=1310, window_size_x=1000)
enter_test_mode(driver)

angelegte_kategorien = []
page_einzelbuchungen_add = EinzelbuchungAdd(driver=driver)

SHARES_INFO_CACHE = '''
{
    "ISIN12345678": {
        "data": [
            {
                "date": "31.05.2021",
                "data": {
                    "Name": "MSCI World",
                    "IndexName": "MSCI World SRI",
                    "Kosten": 0.18,
                    "Regionen": {
                        "USA": 59.76,
                        "JPN": 9.29,
                        "DEU": 4.61,
                        "CHE": 4.17,
                        "CAN": 3.76,
                        "FRA": 3.29,
                        "NLD": 3.13,
                        "GBR": 2.51,
                        "DNK": 2.32,
                        "AUS": 2.14
                    },
                    "Sektoren": {
                        "Konsumg\u00fcter": 15.59,
                        "Gesundheitswesen": 15.41,
                        "Informationstechnologie": 15.34,
                        "Finanzen": 14.51,
                        "Industrieg\u00fcter": 12.49,
                        "Basiskonsumg\u00fcter": 10.68,
                        "Roh- und Grundstoffe": 5.08,
                        "Kommunikationsdienste": 4.89,
                        "Immobilien": 3.76,
                        "Versorgungsunternehmen": 1.47,
                        "Energie": 0.77,
                        "Sonstiges": 0.01
                    }
                }
            }
        ]
    },
    "ISIN22345678": {
        "data": [
            {
                "date": "31.05.2021",
                "data": {
                    "Name": "MSCI EM",
                    "IndexName": "MSCI Em",
                    "Kosten": 0.25,
                    "Regionen": {
                        "CHN": 19.98,
                        "KOR": 13.66,
                        "TWN": 13.4,
                        "ZAF": 11.08,
                        "IND": 9.9,
                        "BRA": 7.44,
                        "MYS": 5.61,
                        "THA": 5.03,
                        "IDN": 4.22,
                        "MEX": 2.73,
                        "QAT": 2.24,
                        "ARE": 1.2,
                        "PHL": 1.0
                    },
                    "Sektoren": {
                        "Finanzen": 29.73,
                        "Konsumg\u00fcter": 24.66,
                        "Kommunikationsdienste": 9.44,
                        "Basiskonsumg\u00fcter": 9.05,
                        "Roh- und Grundstoffe": 7.8,
                        "Gesundheitswesen": 5.88,
                        "Industrieg\u00fcter": 5.1,
                        "Informationstechnologie": 5.05,
                        "Immobilien": 1.4,
                        "Energie": 1.03,
                        "Versorgungsunternehmen": 0.86,
                        "Sonstiges": 0.0
                    }
                }
            }
        ]
    }
}
'''

shares_info_cache = open('shares_info_cache.json', 'w')

shares_info_cache.writelines(SHARES_INFO_CACHE)
shares_info_cache.close()


def dauerauftrag(startdatum,
                 endedatum,
                 name,
                 kategorie,
                 wert,
                 typ='Ausgabe',
                 rhythmus='monatlich'
                 ):
    return {
        'startdatum': startdatum, 'endedatum': endedatum, 'name': name, 'kategorie': kategorie, 'wert': wert,
        'typ': typ, 'rhythmus': rhythmus
    }


def einzelbuchung(datum, name, kategorie, wert):
    return {
        'date': datum,
        'name': name,
        'kategorie': kategorie,
        'wert': wert
    }


def save_fullpage_screenshot(url: str, path: str) -> None:
    large_driver = _launch_head_firefox(window_size_x=4000, window_size_y=1000)
    large_driver.get(url)
    sleep(2)
    # Ref: https://stackoverflow.com/a/52572919/
    original_size = large_driver.get_window_size()
    required_width = large_driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = large_driver.execute_script('return document.body.parentNode.scrollHeight')
    large_driver.set_window_size(required_width, required_height)
    large_driver.get(url)
    sleep(2)
    # driver.save_screenshot(path)  # has scrollbar
    large_driver.find_element(By.TAG_NAME, 'body').screenshot(path)  # avoids scrollbar
    large_driver.set_window_size(original_size['width'], original_size['height'])
    sleep(2)
    close_driver(driver=large_driver)


dauerauftrage = [
    dauerauftrag(
        startdatum=datum('01.01.2019'),
        endedatum=datum('02.12.2019'),
        name='Miete',
        kategorie='Wohnen',
        wert=900
    ),
    dauerauftrag(
        startdatum=datum('01.01.2019'),
        endedatum=datum('02.12.2019'),
        name='Strom',
        kategorie='Wohnen',
        wert=100
    ),
    dauerauftrag(
        startdatum=datum('01.01.2019'),
        endedatum=datum('02.03.2019'),
        name='Heizen',
        kategorie='Wohnen',
        wert=80
    ),
    dauerauftrag(
        startdatum=datum('01.04.2019'),
        endedatum=datum('02.7.2019'),
        name='Heizen',
        kategorie='Wohnen',
        wert=40
    ),
    dauerauftrag(
        startdatum=datum('01.08.2019'),
        endedatum=datum('02.12.2019'),
        name='Heizen',
        kategorie='Wohnen',
        wert=95
    ),
    dauerauftrag(
        startdatum=datum('01.01.2019'),
        endedatum=datum('02.06.2019'),
        name='Gehalt',
        kategorie='Einkommen',
        typ='Einnahme',
        wert=2000
    ),
    dauerauftrag(
        startdatum=datum('01.07.2019'),
        endedatum=datum('02.12.2019'),
        name='Gehalt',
        kategorie='Einkommen',
        typ='Einnahme',
        wert=2100
    ),
    dauerauftrag(
        startdatum=datum('01.01.2019'),
        endedatum=datum('02.12.2019'),
        name='Edeka Monatseinkauf',
        kategorie='Essen',
        wert=150
    ),
    dauerauftrag(
        startdatum=datum('01.01.2019'),
        endedatum=datum('02.12.2019'),
        name='Fitnesstudio',
        kategorie='Sport',
        wert=66
    ),
    dauerauftrag(
        startdatum=datum('01.01.2019'),
        endedatum=datum('02.12.2019'),
        name='60-Euro-Ticket',
        kategorie='Bahn',
        wert=60
    )
]

einzelbuchungen = [
    einzelbuchung(
        datum=datum('14.05.2019'),
        kategorie='Urlaub',
        name='Fahrt in die Berge',
        wert=300
    ),
    einzelbuchung(
        datum=datum('14.05.2019'),
        kategorie='Urlaub',
        name='Fahrt ans Meer',
        wert=800
    ),
    einzelbuchung(
        datum=datum('25.11.2019'),
        kategorie='Geschenke',
        name='Weihnachtsgeschenke',
        wert=50
    ),
    einzelbuchung(
        datum=datum('10.12.2019'),
        kategorie='Geschenke',
        name='Weihnachtsgeschenke',
        wert=200
    ),
    einzelbuchung(
        datum=datum('10.12.2019'),
        kategorie='Essen',
        name='Einkaufen',
        wert=100
    ),
    einzelbuchung(
        datum=datum('10.10.2019'),
        kategorie='Essen',
        name='Einkaufen',
        wert=101
    ),
    einzelbuchung(
        datum=datum('10.5.2019'),
        kategorie='Essen',
        name='Einkaufen',
        wert=40
    ),
    einzelbuchung(
        datum=datum('10.2.2019'),
        kategorie='Essen',
        name='Einkaufen',
        wert=77
    ),
    einzelbuchung(
        datum=datum('08.3.2019'),
        kategorie='Kleidung',
        name='Neue Hosen',
        wert=150
    ), einzelbuchung(
        datum=datum('11.09.2019'),
        kategorie='Kleidung',
        name='Neue Socken',
        wert=100
    ),
]

page_dauerauftrag_add = DauerauftragAdd(driver=driver)
for dauerauftrag in dauerauftrage:
    kategorie = dauerauftrag['kategorie']
    if kategorie not in angelegte_kategorien:
        page_einzelbuchungen_add.visit()
        page_einzelbuchungen_add.define_kategorie(kategorie)
    page_dauerauftrag_add.visit()
    page_dauerauftrag_add.add(**dauerauftrag)

driver.save_screenshot('./dauerauftraege_add.png')

for einzelbuchung in einzelbuchungen:
    kategorie = einzelbuchung['kategorie']
    if kategorie not in angelegte_kategorien:
        page_einzelbuchungen_add.visit()
        page_einzelbuchungen_add.define_kategorie(kategorie)
    page_einzelbuchungen_add.visit()
    page_einzelbuchungen_add.add(**einzelbuchung)

driver.save_screenshot('./einzelbuchungen_add.png')


page_gemeinsame_add = GemeinsamAdd(driver=driver)
page_gemeinsame_abrechnen = GemeinsamAbrechnen(driver=driver)

page_gemeinsame_add.visit()
page_gemeinsame_add.add(
    date=datum('01.03.2019'),
    kategorie='Essen',
    name='Einkauf Edeka',
    wert='100',
    person='test'
)
page_gemeinsame_add.add(
    date=datum('01.03.2019'),
    kategorie='Essen',
    name='Kino',
    wert='50',
    person='Partner'
)
driver.save_screenshot('./add_gemeinsam.png')

page_depot_add = DepotAdd(driver=driver)

page_depot_add.visit()
page_depot_add.add(
    name='Sparkonto',
    typ='Sparkonto'
)
page_depot_add.add(
    name='Hausbank-Depot',
    typ='Depot'
)
page_depot_add.add(
    name='Fintex-Depot',
    typ='Depot'
)

page_depotwert_add = DepotwertAdd(driver=driver)
page_depotwert_add.visit()
page_depotwert_add.add(
    name='MSCI World',
    isin='ISIN12345678'
)

page_depotwert_add.add(
    name='MSCI EM',
    isin='ISIN22345678'
)

page_order_add = OrderAdd(driver=driver)
page_order_add.visit()
page_order_add.add(
    name='Regelsparen',
    datum=datum('01.01.2018'),
    wert=1000,
    depotwert='MSCI World (ISIN12345678)',
    konto='Hausbank-Depot',
    kauf=True
)
page_order_add.add(
    name='Regelsparen',
    datum=datum('01.01.2019'),
    wert=1000,
    depotwert='MSCI World (ISIN12345678)',
    konto='Hausbank-Depot',
    kauf=True
)

page_order_add.add(
    name='Regelsparen',
    datum=datum('01.02.2018'),
    wert=200,
    depotwert='MSCI EM (ISIN22345678)',
    konto='Fintex-Depot',
    kauf=True
)
page_order_add.add(
    name='Regelsparen',
    datum=datum('01.02.2019'),
    wert=200,
    depotwert='MSCI EM (ISIN22345678)',
    konto='Fintex-Depot',
    kauf=True
)

page_sparbuchung_add = SparbuchungAdd(driver=driver)
page_sparbuchung_add.visit()
page_sparbuchung_add.add(
    datum=datum('01.01.2017'),
    wert=2000,
    name='Notgroschen',
    konto='Sparkonto',
    einzahlung=True,
    typ='Manueller Auftrag'
)

page_depotauszug_add = DepotauszugAdd(driver=driver)

page_depotauszug_add.visit()
page_depotauszug_add.add(
    datum=datum('01.12.2018'),
    depotwert='ISIN12345678',
    wert=1100,
    konto='Hausbank-Depot',
)
page_depotauszug_add.add(
    datum=datum('01.10.2019'),
    depotwert='ISIN12345678',
    wert=2300,
    konto='Hausbank-Depot',
)

page_depotauszug_add.add(
    datum=datum('01.12.2018'),
    depotwert='ISIN22345678',
    wert=230,
    konto='Fintex-Depot',
)
page_depotauszug_add.add(
    datum=datum('01.10.2019'),
    depotwert='ISIN22345678',
    wert=500,
    konto='Fintex-Depot',
)

driver.save_screenshot('./sparen_add_depotauszug.png')

driver.get('http://localhost:5000/uebersicht_sparkontos/')
driver.save_screenshot('./sparen_uebersicht_sparkontos.png')
driver.get('http://localhost:5000/uebersicht_depotwerte/')
driver.save_screenshot('./sparen_uebersicht_depotwerte.png')
driver.get('http://localhost:5000/dauerauftraguebersicht/')
driver.save_screenshot('./uebersicht_dauerauftraege.png')
sleep(2)
driver.get('http://localhost:5000/uebersicht/')
driver.save_screenshot('./uebersicht_einzelbuchungen.png')
driver.get('http://localhost:5000')
sleep(2)
driver.save_screenshot('./dashboard.png')

save_fullpage_screenshot(url=page_gemeinsame_abrechnen.URL, path='./gemeinsam_abrechnen.png')

save_fullpage_screenshot(url='http://localhost:5000/jahresuebersicht/',
                         path='./uebersicht_jahr.png')
save_fullpage_screenshot(url='http://localhost:5000/monatsuebersicht/',
                         path='./uebersicht_monat.png')

save_fullpage_screenshot('http://localhost:5000/uebersicht_etfs/', './sparen_uebersicht_etfs.png')
save_fullpage_screenshot('http://localhost:5000/sparen/', './sparen_uebersicht.png')
