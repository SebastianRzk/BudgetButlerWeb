from butler_offline.core.database import Database


def test_taint_should_increase_taint_number():
    db = Database()

    assert db.taint_number() == 0
    db.taint()
    assert db.taint_number() == 1


def test_is_tainted_should_return_false_when_tainted():
    db = Database()

    assert not db.is_tainted()
    db.taint()
    assert db.is_tainted()


def test_tain_number_should_include_dauerauftraege():
    db = Database()

    assert db.taint_number() == 0
    db.dauerauftraege.taint()
    assert db.taint_number() == 1


def test_taint_number_should_include_gemeinsame_buchungen():
    db = Database()

    assert db.taint_number() == 0
    db.gemeinsamebuchungen.taint()
    assert db.taint_number() == 1


def test_taint_number_should_include_sparbuchungen():
    db = Database()

    assert db.taint_number() == 0
    db.sparbuchungen.taint()
    assert db.taint_number() == 1


def test_tain_number_should_include_einzelbuchungen():
    db = Database()

    assert db.taint_number() == 0
    db.einzelbuchungen.taint()
    assert db.taint_number() == 1


def test_tain_number_should_include_kontos():
    db = Database()

    assert db.taint_number() == 0
    db.sparkontos.taint()
    assert db.taint_number() == 1


def test_tain_number_should_include_depotwerte():
    db = Database()

    assert db.taint_number() == 0
    db.depotwerte.taint()
    assert db.taint_number() == 1


def test_tain_number_should_include_order():
    db = Database()

    assert db.taint_number() == 0
    db.order.taint()
    assert db.taint_number() == 1


def test_tain_number_should_include_depotauszuege():
    db = Database()

    assert db.taint_number() == 0
    db.depotauszuege.taint()
    assert db.taint_number() == 1


def test_tain_number_should_include_orderdauerauftraege():
    db = Database()

    assert db.taint_number() == 0
    db.orderdauerauftrag.taint()
    assert db.taint_number() == 1

