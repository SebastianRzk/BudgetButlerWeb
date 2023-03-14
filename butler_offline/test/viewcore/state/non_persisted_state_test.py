from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.state import persisted_state
from butler_offline.core.database import Database


def clear_context():
    non_persisted_state.CONTEXT = {}
    persisted_state.DATABASE_INSTANCE = Database('db')


def test_einzelbuchungen():
    clear_context()

    assert non_persisted_state.get_changed_einzelbuchungen() == []

    non_persisted_state.add_changed_einzelbuchungen('demo')

    assert non_persisted_state.get_changed_einzelbuchungen() == ['demo']


def test_dauerauftraege():
    clear_context()

    assert non_persisted_state.get_changed_dauerauftraege() == []

    non_persisted_state.add_changed_dauerauftraege('demo')

    assert non_persisted_state.get_changed_dauerauftraege() == ['demo']


def test_gemeinsame_buchungen():
    clear_context()

    assert non_persisted_state.get_changed_gemeinsamebuchungen() == []

    non_persisted_state.add_changed_gemeinsamebuchungen('demo')

    assert non_persisted_state.get_changed_gemeinsamebuchungen() == ['demo']


def test_sparbuchungen():
    clear_context()

    assert non_persisted_state.get_changed_sparbuchungen() == []

    non_persisted_state.add_changed_sparbuchungen('demo')

    assert non_persisted_state.get_changed_sparbuchungen() == ['demo']


def test_sparkontos():
    clear_context()

    assert non_persisted_state.get_changed_sparkontos() == []

    non_persisted_state.add_changed_sparkontos('demo')

    assert non_persisted_state.get_changed_sparkontos() == ['demo']


def test_depotwerte():
    clear_context()

    assert non_persisted_state.get_changed_depotwerte() == []

    non_persisted_state.add_changed_depotwerte('demo')

    assert non_persisted_state.get_changed_depotwerte() == ['demo']


def test_order():
    clear_context()

    assert non_persisted_state.get_changed_order() == []

    non_persisted_state.add_changed_order('demo')

    assert non_persisted_state.get_changed_order() == ['demo']


def test_depotauszuege():
    clear_context()

    assert non_persisted_state.get_changed_depotauszuege() == []

    non_persisted_state.add_changed_depotauszuege('demo')

    assert non_persisted_state.get_changed_depotauszuege() == ['demo']

