from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.state import persisted_state
from butler_offline.core.database import Database
from butler_offline.test.viewcore.state.non_persisted_state.einzelbuchung_changed_test_factory import \
    EINZELBUCHUNG_ADDED_CHANGE


def clear_context():
    non_persisted_state.CONTEXT = non_persisted_state.NonPersistedContext()
    persisted_state.DATABASE_INSTANCE = Database('db')


def test_einzelbuchungen():
    clear_context()

    assert non_persisted_state.get_changed_einzelbuchungen() == []

    non_persisted_state.add_changed_einzelbuchungen(EINZELBUCHUNG_ADDED_CHANGE)

    assert non_persisted_state.get_changed_einzelbuchungen() == [EINZELBUCHUNG_ADDED_CHANGE]


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

