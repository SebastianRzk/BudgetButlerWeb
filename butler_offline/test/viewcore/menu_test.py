from butler_offline.viewcore.menu import get_menu_list, EINZELBUCHUNGEN_SUBMENU_NAME, GEMEINSAME_FINANZEN_SUBMENU_NAME, SPAREN_SUBMENU_NAME, EINSTELLUNGEN_SUBMENU_NAME


def test_menu_has_a_fixed_order():
    menu = get_menu_list()

    assert list(menu.keys()) == [
        EINZELBUCHUNGEN_SUBMENU_NAME,
        GEMEINSAME_FINANZEN_SUBMENU_NAME,
        SPAREN_SUBMENU_NAME,
        EINSTELLUNGEN_SUBMENU_NAME]


def test_submenu_sizes():
    menu = get_menu_list()

    assert len(menu[EINZELBUCHUNGEN_SUBMENU_NAME]) == 8
    assert len(menu[GEMEINSAME_FINANZEN_SUBMENU_NAME]) == 5
    assert len(menu[SPAREN_SUBMENU_NAME]) == 14
    assert len(menu[EINSTELLUNGEN_SUBMENU_NAME]) == 2
