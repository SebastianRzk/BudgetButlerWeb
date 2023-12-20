from butler_offline.viewcore.context.builder import PageContext
from butler_offline.viewcore.requirements import KEINE_BUCHUNGEN_ERFASST_MESSAGE, \
    KEINE_GEMEINSAME_BUCHUNGEN_ERFASST_MESSAGE, KEINE_DAUERAUFTRAEGE_ERFASST_MESSAGE, KEINE_DEPOTS_ERFASST_MESSAGE, \
    KEINE_DEPOTWERTE_ERFASST_MESSAGE, KEINE_SPARFAEHIGEN_KONTOS_ERFASST_MESSAGE, KEINE_DEPOTAUSZUEGE_ERFASST_MESSAGE, \
    KEINE_ETFS_ERFASST_MESSAGE, KEINE_ORDER_ERFASST_MESSAGE, KEINE_ORDER_DAUERAUFTRAEGE_ERFASST_MESSAGE, \
    KEINE_SPARBUCHUNGEN_ERFASST_MESSAGE, DATENBANK_LEER_MESSAGE


def assert_keine_message_set(result: PageContext):
    assert not result.get_info_messages()


def assert_info_message_keine_buchungen_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_BUCHUNGEN_ERFASST_MESSAGE


def assert_info_message_keine_depots_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_DEPOTS_ERFASST_MESSAGE


def assert_info_message_keine_depotwerte_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_DEPOTWERTE_ERFASST_MESSAGE


def assert_info_message_keine_order_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_ORDER_ERFASST_MESSAGE


def assert_info_message_nichts_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == DATENBANK_LEER_MESSAGE


def assert_info_message_keine_order_dauerauftraege_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_ORDER_DAUERAUFTRAEGE_ERFASST_MESSAGE


def assert_info_message_keine_depotauszuege_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_DEPOTAUSZUEGE_ERFASST_MESSAGE


def assert_info_message_keine_etfs_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_ETFS_ERFASST_MESSAGE


def assert_info_message_dauerauftraege_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_DAUERAUFTRAEGE_ERFASST_MESSAGE


def assert_info_message_keine_gemeinsame_buchungen_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_GEMEINSAME_BUCHUNGEN_ERFASST_MESSAGE


def assert_info_message_kein_sparkonto_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_SPARFAEHIGEN_KONTOS_ERFASST_MESSAGE


def assert_info_message_keine_sparbuchungen_erfasst_in_context(result: PageContext):
    assert len(result.get_info_messages()) == 1
    assert result.get_info_messages()[0].content() == KEINE_SPARBUCHUNGEN_ERFASST_MESSAGE
