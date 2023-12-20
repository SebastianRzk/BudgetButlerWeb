from butler_offline.core.database import Database


def test_taint_should_increase_taint_number():
    database = Database()

    assert database.taint_number() == 0
    database.taint()
    assert database.taint_number() == 1


def test_is_tainted_should_return_false_when_tainted():
    database = Database()

    assert not database.is_tainted()
    database.taint()
    assert database.is_tainted()


def test_taint_number_should_include_dauerauftraege():
    database = Database()

    assert database.taint_number() == 0
    database.dauerauftraege.taint()
    assert database.taint_number() == 1


def test_taint_number_should_include_gemeinsame_buchungen():
    database = Database()

    assert database.taint_number() == 0
    database.gemeinsamebuchungen.taint()
    assert database.taint_number() == 1


def test_taint_number_should_include_sparbuchungen():
    database = Database()

    assert database.taint_number() == 0
    database.sparbuchungen.taint()
    assert database.taint_number() == 1


def test_taint_number_should_include_einzelbuchungen():
    database = Database()

    assert database.taint_number() == 0
    database.einzelbuchungen.taint()
    assert database.taint_number() == 1


def test_taint_number_should_include_kontos():
    database = Database()

    assert database.taint_number() == 0
    database.sparkontos.taint()
    assert database.taint_number() == 1


def test_taint_number_should_include_depotwerte():
    database = Database()

    assert database.taint_number() == 0
    database.depotwerte.taint()
    assert database.taint_number() == 1


def test_taint_number_should_include_order():
    database = Database()

    assert database.taint_number() == 0
    database.order.taint()
    assert database.taint_number() == 1


def test_taint_number_should_include_depotauszuege():
    database = Database()

    assert database.taint_number() == 0
    database.depotauszuege.taint()
    assert database.taint_number() == 1


def test_taint_number_should_include_orderdauerauftraege():
    database = Database()

    assert database.taint_number() == 0
    database.orderdauerauftrag.taint()
    assert database.taint_number() == 1

