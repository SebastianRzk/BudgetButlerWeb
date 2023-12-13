from butler_offline.viewcore.template import fa
from butler_offline.test.viewcore.state.non_persisted_state.dauerauftrag_changed_test_factory import \
    DAUERAUFTRAG_EDITIERT_CHANGE, DAUERAUFTRAG_ADDED_CHANGE, DAUERAUFTRAG_EDITIERT_CHANGE_STR, \
    DAUERAUFTRAG_ADDED_CHANGE_STR


def test_dauerauftrag_added_str():
    assert str(DAUERAUFTRAG_ADDED_CHANGE) == DAUERAUFTRAG_ADDED_CHANGE_STR


def test_dauerauftrag_added_repr():
    assert repr(DAUERAUFTRAG_ADDED_CHANGE) == DAUERAUFTRAG_ADDED_CHANGE_STR


def test_dauerauftrag_editiert_str():
    assert str(DAUERAUFTRAG_EDITIERT_CHANGE_STR) == DAUERAUFTRAG_EDITIERT_CHANGE_STR


def test_dauerauftrag_editiert_repr():
    assert repr(DAUERAUFTRAG_EDITIERT_CHANGE) == DAUERAUFTRAG_EDITIERT_CHANGE_STR


def test_dauerauftrag_editiert_should_have_fa_pencil():
    assert DAUERAUFTRAG_EDITIERT_CHANGE.fa == fa.fa_pencil


def test_dauerauftrag_added_should_have_fa_plus():
    assert DAUERAUFTRAG_ADDED_CHANGE.fa == fa.fa_plus
