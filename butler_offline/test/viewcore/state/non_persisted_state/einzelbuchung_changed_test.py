from butler_offline.viewcore.template import fa
from butler_offline.test.viewcore.state.non_persisted_state.einzelbuchung_changed_test_factory import \
    EINZELBUCHUNG_EDITIERT_CHANGE, EINZELBUCHUNG_ADDED_CHANGE, EINZELBUCHUNG_EDITIERT_CHANGE_STR, \
    EINZELBUCHUNG_ADDED_CHANGE_STR


def test_einzelbuchung_added_str():
    assert str(EINZELBUCHUNG_ADDED_CHANGE) == EINZELBUCHUNG_ADDED_CHANGE_STR


def test_einzelbuchung_added_repr():
    assert repr(EINZELBUCHUNG_ADDED_CHANGE) == EINZELBUCHUNG_ADDED_CHANGE_STR


def test_einzelbuchung_editiert_str():
    assert str(EINZELBUCHUNG_EDITIERT_CHANGE_STR) == EINZELBUCHUNG_EDITIERT_CHANGE_STR


def test_einzelbuchung_editiert_repr():
    assert repr(EINZELBUCHUNG_EDITIERT_CHANGE) == EINZELBUCHUNG_EDITIERT_CHANGE_STR


def test_einzelbuchung_editiert_should_have_fa_pencil():
    assert EINZELBUCHUNG_EDITIERT_CHANGE.fa == fa.fa_pencil


def test_einzelbuchung_added_should_have_fa_plus():
    assert EINZELBUCHUNG_ADDED_CHANGE.fa == fa.fa_plus
