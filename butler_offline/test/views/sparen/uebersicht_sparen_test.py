from butler_offline.viewcore.state import persisted_state
from butler_offline.test.request_stubs import GetRequest
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.views.sparen import uebersicht_sparen
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.order import Order
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.renderhelper import Betrag, BetragListe
from butler_offline.test.test import assert_info_message_nichts_erfasst_in_context, assert_keine_message_set


def test_index_should_be_secured_by_requesthandler():
    def handle():
        uebersicht_sparen.index(request=GetRequest())

    result = run_in_mocked_handler(handle)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/uebersicht_sparen.html']


def test_transaction_id_should_not_be_in_context():
    context = uebersicht_sparen.handle_request(GetRequest(), get_test_data())
    assert context


def get_test_data() -> uebersicht_sparen.SparenUebersichtContext:
    sparkontos = Kontos()
    sparkontos.add(kontoname='demokonto1', kontotyp=sparkontos.TYP_SPARKONTO)
    sparkontos.add(kontoname='demokonto2', kontotyp=sparkontos.TYP_DEPOT)

    sparbuchungen = Sparbuchungen()
    sparbuchungen.add(datum('01.01.2020'), 'testname', 100, sparbuchungen.TYP_MANUELLER_AUFTRAG, 'demokonto1')
    sparbuchungen.add(datum('01.01.2020'), 'testname', 10, sparbuchungen.TYP_ZINSEN, 'demokonto1')

    depotwerte = Depotwerte()
    depotwerte.add(name='demoname', isin='demoisin', typ=depotwerte.TYP_ETF)

    order = Order()
    order.add(datum('01.01.2020'), 'testname', 'demokonto2', 'demoisin', 999)

    depotauszuege = Depotauszuege()
    depotauszuege.add(datum('02.01.2020'), 'demoisin', 'demokonto2', 990)

    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2020'), '1', '1', 1)

    return uebersicht_sparen.SparenUebersichtContext(
        einzelbuchungen=einzelbuchungen,
        kontos=sparkontos,
        orderdauerauftrag=OrderDauerauftrag(),
        depotwerte=depotwerte,
        sparbuchungen=sparbuchungen,
        depotauszuege=depotauszuege,
        order=order,
    )


def get_typen_test_data() -> uebersicht_sparen.SparenUebersichtContext:
    test_data_context = get_test_data()
    test_data_context.depotwerte().add(name='demoname2', isin='demoisin2', typ=test_data_context.depotwerte().TYP_ETF)
    test_data_context.depotwerte().add(name='demoname3', isin='demoisin3', typ=test_data_context.depotwerte().TYP_FOND)
    test_data_context.order().add(datum('01.01.2020'), 'testname', 'demokonto2', 'demoisin2', 888)
    test_data_context.depotauszeuge().add(datum('02.01.2020'), 'demoisin2', 'demokonto2', 880)
    test_data_context.order().add(datum('01.01.2020'), 'testname', 'demokonto2', 'demoisin3', 777)
    test_data_context.depotauszeuge().add(datum('02.01.2020'), 'demoisin3', 'demokonto2', 770)
    return test_data_context


def test_should_list_kontos():
    result = uebersicht_sparen.handle_request(GetRequest(), get_test_data())

    assert result.get('kontos') == [
        {
            'index': 0,
            'name': 'demokonto2',
            'kontotyp': 'Depot',
            'wert': Betrag(990),
            'aufbuchungen': Betrag(999),
            'difference': Betrag(-9),
            'color': '#f56954',
            'difference_is_negativ': True
        },
        {
            'index': 1,
            'name': 'demokonto1',
            'kontotyp': 'Sparkonto',
            'wert': Betrag(110),
            'aufbuchungen': Betrag(100),
            'difference': Betrag(10),
            'color': '#3c8dbc',
            'difference_is_negativ': False
        }
    ]


def test_gesamt():
    result = uebersicht_sparen.handle_request(GetRequest(), get_test_data())

    assert result.get('gesamt') == {
        'wert': Betrag(1100),
        'aufbuchungen': Betrag(1099),
        'difference': Betrag(1),
        'difference_is_negativ': False
    }


def test_typen():
    result = uebersicht_sparen.handle_request(GetRequest(), get_typen_test_data())

    assert result.get('typen') == [
        {'aufbuchungen': Betrag(100),
         'color': '#39CCCC',
         'difference': Betrag(10),
         'name': 'Sparkonto',
         'wert': Betrag(110)},
        {'aufbuchungen': Betrag(0),
         'color': '#d2d6de',
         'difference': Betrag(0),
         'name': 'Genossenschafts-Anteile',
         'wert': Betrag(0)},
        {'aufbuchungen': Betrag(1887),
         'color': '#00a65a',
         'difference': Betrag(-17),
         'name': 'ETF',
         'wert': Betrag(1870)},
        {'aufbuchungen': Betrag(777),
         'color': '#f39c12',
         'difference': Betrag(-7),
         'name': 'Fond',
         'wert': Betrag(770)},
    ]


def test_konto_diagramm():
    result = uebersicht_sparen.handle_request(GetRequest(), get_test_data())

    assert result.get('konto_diagramm') == {
        'colors': ['#f56954', '#3c8dbc'],
        'datasets': BetragListe([Betrag(90.00), Betrag(10.00)]),
        'labels': ['demokonto2', 'demokonto1'],
    }


def test_typen_diagramm():
    result = uebersicht_sparen.handle_request(GetRequest(), get_typen_test_data())

    assert result.get('typen_diagramm') == {
        'colors': ['#39CCCC', '#d2d6de', '#00a65a', '#f39c12'],
        'datasets': BetragListe([Betrag(4), Betrag(0), Betrag(68), Betrag(28)]),
        'labels': ['Sparkonto', 'Genossenschafts-Anteile', 'ETF', 'Fond'],
    }


def test_init_with_empty_database_should_show_message():
    persisted_state.DATABASE_INSTANCE = None

    context = uebersicht_sparen.handle_request(GetRequest(), uebersicht_sparen.SparenUebersichtContext(
        einzelbuchungen=Einzelbuchungen(),
        depotauszuege=Depotauszuege(),
        kontos=Kontos(),
        depotwerte=Depotwerte(),
        sparbuchungen=Sparbuchungen(),
        orderdauerauftrag=OrderDauerauftrag(),
        order=Order()
    ))

    assert context.is_ok()
    assert_info_message_nichts_erfasst_in_context(result=context)


def test_init_filled_database():
    context = uebersicht_sparen.handle_request(GetRequest(), get_test_data())
    assert_keine_message_set(result=context)


def test_info():
    sparkontos = Kontos()
    sparkontos.add(kontoname='demodepot1', kontotyp=sparkontos.TYP_DEPOT)
    sparkontos.add(kontoname='demodepot2', kontotyp=sparkontos.TYP_DEPOT)
    sparkontos.add(kontoname='demodepot3', kontotyp=sparkontos.TYP_DEPOT)

    depotwerte = Depotwerte()
    depotwerte.add(name='demoname', isin='demoisin', typ=depotwerte.TYP_ETF)

    order = Order()
    order.add(datum('01.01.2020'), 'testname', 'demodepot1', 'demoisin', 999)
    order.add(datum('01.01.2020'), 'testname', 'demodepot2', 'demoisin', 999)

    depotauszuege = Depotauszuege()
    depotauszuege.add(datum('02.01.2020'), 'demoisin', 'demodepot1', 990)
    depotauszuege.add(datum('02.01.2019'), 'demoisin', 'demodepot2', 0)

    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2020'), '1', '1', 1)

    result = uebersicht_sparen.handle_request(
        GetRequest(),
        uebersicht_sparen.SparenUebersichtContext(
            einzelbuchungen=einzelbuchungen,
            orderdauerauftrag=OrderDauerauftrag(),
            order=order,
            depotwerte=depotwerte,
            kontos=sparkontos,
            sparbuchungen=Sparbuchungen(),
            depotauszuege=depotauszuege
        )
    )

    assert result.get('general_infos') == {
        'kontos':
            [
                {
                    'konto': 'demodepot1',
                    'letzter_auszug': '02.01.2020',
                    'letzte_order': '01.01.2020',
                    'warning': False
                },
                {
                    'konto': 'demodepot2',
                    'letzter_auszug': '02.01.2019',
                    'letzte_order': '01.01.2020',
                    'warning': True
                },
                {
                    'konto': 'demodepot3',
                    'letzter_auszug': 'fehlend',
                    'letzte_order': '',
                    'warning': True}]}


def test_order_typ():

    sparkontos = Kontos()
    sparkontos.add(kontoname='demodepot1', kontotyp=sparkontos.TYP_DEPOT)

    depotwerte = Depotwerte()
    depotwerte.add(name='demoname', isin='demoisin', typ=depotwerte.TYP_ETF)

    order = Order()
    order.add(datum('01.01.2020'), 'testname', 'demodepot1', 'demoisin', 100)

    orderdauerauftrag = OrderDauerauftrag()
    orderdauerauftrag.add(
        datum('01.01.2020'),
        datum('02.02.2020'),
        name='1name',
        rhythmus='monatlich',
        depotwert='demoisin',
        konto='demodepot1',
        wert=33
    )
    order.append_row(orderdauerauftrag.get_all_order_until_today())

    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2020'), '1', '1', 1)

    result = uebersicht_sparen.handle_request(
        GetRequest(),
        uebersicht_sparen.SparenUebersichtContext(
            einzelbuchungen=einzelbuchungen,
            order=order,
            kontos=Kontos(),
            depotwerte=depotwerte,
            depotauszuege=Depotauszuege(),
            sparbuchungen=Sparbuchungen(),
            orderdauerauftrag=orderdauerauftrag
        )
    )

    assert result.get('order_typ') == {
        'manual': Betrag(100),
        'dauerauftrag': Betrag(66),
    }


def test_aktuelle_dauerauftraege():
    sparkontos = Kontos()
    sparkontos.add(kontoname='demodepot1', kontotyp=sparkontos.TYP_DEPOT)

    depotwerte = Depotwerte()
    depotwerte.add(name='DemoName1', isin='is1', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='DemoName2', isin='is2', typ=depotwerte.TYP_ETF)

    orderdauerauftrag = OrderDauerauftrag()
    orderdauerauftrag.add(
        datum('01.01.2020'),
        datum('02.02.2050'),
        name='1name',
        rhythmus='monatlich',
        depotwert='is1',
        konto='demodepot1',
        wert=100
    )
    orderdauerauftrag.add(
        datum('01.01.2020'),
        datum('02.02.2050'),
        name='1name',
        rhythmus='monatlich',
        depotwert='is2',
        konto='demodepot1',
        wert=50
    )

    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('01.01.2020'), '1', '1', 1)

    result = uebersicht_sparen.handle_request(
        GetRequest(),
        context=uebersicht_sparen.SparenUebersichtContext(
            einzelbuchungen=einzelbuchungen,
            orderdauerauftrag=orderdauerauftrag,
            kontos=sparkontos,
            depotwerte=depotwerte,
            depotauszuege=Depotauszuege(),
            sparbuchungen=Sparbuchungen(),
            order=Order()
        )
    )

    assert result.get('monatlich') == {
        'colors': ['#3c8dbc', '#f56954'],
        'einzelwerte': [{'color': '#3c8dbc', 'name': 'DemoName1 (is1)', 'wert': Betrag(100)},
                        {'color': '#f56954', 'name': 'DemoName2 (is2)', 'wert': Betrag(50)}],
        'namen': ['DemoName1 (is1)', 'DemoName2 (is2)'],
        'werte': BetragListe([Betrag(100), Betrag(50)])
    }
