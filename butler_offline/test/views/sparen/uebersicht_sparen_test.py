from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.core import file_system
from butler_offline.views.sparen import uebersicht_sparen
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german as datum


def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    request_handler.stub_me()


def test_transaction_id_should_be_in_context():
    set_up()
    add_test_data()
    context = uebersicht_sparen.index(GetRequest())
    assert 'ID' in context


def add_test_data():
    sparkontos = persisted_state.database_instance().sparkontos
    sparkontos.add(kontoname='demokonto1', kontotyp=sparkontos.TYP_SPARKONTO)
    sparkontos.add(kontoname='demokonto2', kontotyp=sparkontos.TYP_DEPOT)
    sparbuchungen = persisted_state.database_instance().sparbuchungen
    sparbuchungen.add(datum('01.01.2020'), 'testname', 100, sparbuchungen.TYP_MANUELLER_AUFTRAG, 'demokonto1')
    sparbuchungen.add(datum('01.01.2020'), 'testname', 10, sparbuchungen.TYP_ZINSEN, 'demokonto1')

    persisted_state.database_instance().depotwerte.add('demoname', 'demoisin')
    persisted_state.database_instance().order.add(datum('01.01.2020'), 'testname', 'demokonto2', 'demoisin', 999)
    persisted_state.database_instance().depotauszuege.add(datum('02.01.2020'), 'demoisin', 'demokonto2', 990)

    persisted_state.database_instance().einzelbuchungen.add(datum('01.01.2020'), '1', '1', 1)


def test_should_list_kontos():
    set_up()
    add_test_data()

    result = uebersicht_sparen.index(GetRequest())

    assert result['kontos'] == [
        {
            'index': 0,
            'name': 'demokonto2',
            'kontotyp': 'Depot',
            'wert': 990,
            'aufbuchungen': 999,
            'difference': -9,
            'wert_str': '990,00',
            'aufbuchungen_str': '999,00',
            'difference_str': '-9,00',
            'color': '#f56954',
            'difference_is_negativ': True
        },
        {
            'index': 1,
            'name': 'demokonto1',
            'kontotyp': 'Sparkonto',
            'wert': 110,
            'aufbuchungen': 100,
            'difference': 10,
            'wert_str': '110,00',
            'aufbuchungen_str': '100,00',
            'difference_str': '10,00',
            'color': '#3c8dbc',
            'difference_is_negativ': False
        }
    ]


def test_gesamt():
    set_up()
    add_test_data()

    result = uebersicht_sparen.index(GetRequest())

    assert result['gesamt'] == {
        'wert': 1100,
        'aufbuchungen': 1099,
        'difference': 1,
        'wert_str': '1100,00',
        'aufbuchungen_str': '1099,00',
        'difference_str': '1,00',
        'difference_is_negativ': False
    }


def test_typen():
    set_up()
    add_test_data()

    result = uebersicht_sparen.index(GetRequest())

    assert result['typen'] == [
        {'aufbuchungen': 100,
         'aufbuchungen_str': '100,00',
         'difference': 10,
         'difference_str': '10,00',
         'wert': 110,
         'wert_str': '110,00',
         'color': '#00a65a',
         'name': 'Sparkonto'},
        {'aufbuchungen': 0,
         'aufbuchungen_str': '0,00',
         'difference': 0,
         'difference_str': '0,00',
         'wert': 0,
         'wert_str': '0,00',
         'color': '#f56954',
         'name': 'Genossenschafts-Anteile'},
        {'aufbuchungen': 999,
         'aufbuchungen_str': '999,00',
         'difference': -9,
         'difference_str': '-9,00',
         'wert': 990,
         'wert_str': '990,00',
         'color': '#3c8dbc',
         'name': 'Depot'},
    ]


def test_konto_diagramm():
    set_up()
    add_test_data()

    result = uebersicht_sparen.index(GetRequest())

    assert result['konto_diagramm'] == {
        'colors': ['#f56954', '#3c8dbc'],
        'datasets': ['90.00', '10.00'],
        'labels': ['demokonto2', 'demokonto1'],
    }


def test_typen_diagramm():
    set_up()
    add_test_data()

    result = uebersicht_sparen.index(GetRequest())

    assert result['typen_diagramm'] == {
        'colors': ['#00a65a', '#f56954', '#3c8dbc'],
        'datasets': ['10.00', '0.00', '90.00'],
        'labels': ['Sparkonto', 'Genossenschafts-Anteile', 'Depot'],
    }


def test_init_with_empty_database():
    set_up()
    persisted_state.DATABASE_INSTANCE = None

    context = uebersicht_sparen.index(GetRequest())

    assert '%Errortext' in context
    assert context['%Errortext'] == 'Bitte erfassen Sie zuerst eine Einzelbuchung.'


def test_init_filled_database():
    set_up()
    add_test_data()
    uebersicht_sparen.index(GetRequest())


def test_info():
    set_up()

    sparkontos = persisted_state.database_instance().sparkontos
    sparkontos.add(kontoname='demodepot1', kontotyp=sparkontos.TYP_DEPOT)
    sparkontos.add(kontoname='demodepot2', kontotyp=sparkontos.TYP_DEPOT)
    sparkontos.add(kontoname='demodepot3', kontotyp=sparkontos.TYP_DEPOT)

    persisted_state.database_instance().depotwerte.add('demoname', 'demoisin')
    persisted_state.database_instance().order.add(datum('01.01.2020'), 'testname', 'demodepot1', 'demoisin', 999)
    persisted_state.database_instance().order.add(datum('01.01.2020'), 'testname', 'demodepot2', 'demoisin', 999)
    persisted_state.database_instance().depotauszuege.add(datum('02.01.2020'), 'demoisin', 'demodepot1', 990)
    persisted_state.database_instance().depotauszuege.add(datum('02.01.2019'), 'demoisin', 'demodepot2', 0)

    persisted_state.database_instance().einzelbuchungen.add(datum('01.01.2020'), '1', '1', 1)

    result = uebersicht_sparen.index(GetRequest())

    assert result['general_infos'] == {
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
    set_up()

    sparkontos = persisted_state.database_instance().sparkontos
    sparkontos.add(kontoname='demodepot1', kontotyp=sparkontos.TYP_DEPOT)

    persisted_state.database_instance().depotwerte.add('demoname', 'demoisin')
    persisted_state.database_instance().order.add(datum('01.01.2020'), 'testname', 'demodepot1', 'demoisin', 100)
    persisted_state.database_instance().orderdauerauftrag.add(
        datum('01.01.2020'),
        datum('02.02.2020'),
        name='1name',
        rhythmus='monatlich',
        depotwert='demoisin',
        konto='demodepot1',
        wert=33
    )
    persisted_state.database_instance().refresh()

    persisted_state.database_instance().einzelbuchungen.add(datum('01.01.2020'), '1', '1', 1)

    result = uebersicht_sparen.index(GetRequest())

    assert result['order_typ'] == {
        'manual': '100,00',
        'dauerauftrag': '66,00',
        'manual_raw': '100.00',
        'dauerauftrag_raw': '66.00'
    }


def test_aktuelle_dauerauftraege():
    set_up()

    sparkontos = persisted_state.database_instance().sparkontos
    sparkontos.add(kontoname='demodepot1', kontotyp=sparkontos.TYP_DEPOT)

    persisted_state.database_instance().depotwerte.add('DemoName1', 'is1')
    persisted_state.database_instance().depotwerte.add('DemoName2', 'is2')
    persisted_state.database_instance().orderdauerauftrag.add(
        datum('01.01.2020'),
        datum('02.02.2050'),
        name='1name',
        rhythmus='monatlich',
        depotwert='is1',
        konto='demodepot1',
        wert=100
    )
    persisted_state.database_instance().orderdauerauftrag.add(
        datum('01.01.2020'),
        datum('02.02.2050'),
        name='1name',
        rhythmus='monatlich',
        depotwert='is2',
        konto='demodepot1',
        wert=50
    )

    persisted_state.database_instance().einzelbuchungen.add(datum('01.01.2020'), '1', '1', 1)

    result = uebersicht_sparen.index(GetRequest())

    assert result['monatlich'] == {
        'colors': ['#3c8dbc', '#f56954'],
        'einzelwerte': [{'color': '#3c8dbc', 'name': 'DemoName1 (is1)', 'wert': '100,00'},
                      {'color': '#f56954', 'name': 'DemoName2 (is2)', 'wert': '50,00'}],
        'namen': ['DemoName1 (is1)', 'DemoName2 (is2)'],
        'werte': ['100.00', '50.00']
    }



