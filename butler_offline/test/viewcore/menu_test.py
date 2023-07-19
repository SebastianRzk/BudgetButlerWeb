from butler_offline.viewcore.menu import get_menu_list, EINZELBUCHUNGEN_SUBMENU_NAME, GEMEINSAME_FINANZEN_SUBMENU_NAME, SPAREN_SUBMENU_NAME, EINSTELLUNGEN_SUBMENU_NAME


def test_menu_has_a_fixed_order():
    menu = get_menu_list('Test_User')

    assert list(menu.keys()) == [
        EINZELBUCHUNGEN_SUBMENU_NAME,
        GEMEINSAME_FINANZEN_SUBMENU_NAME,
        SPAREN_SUBMENU_NAME,
        EINSTELLUNGEN_SUBMENU_NAME]


def test_submenu_sizes():
    menu = get_menu_list('Test_User')

    assert len(menu[EINZELBUCHUNGEN_SUBMENU_NAME]) == 8
    assert len(menu[GEMEINSAME_FINANZEN_SUBMENU_NAME]) == 5
    assert len(menu[SPAREN_SUBMENU_NAME]) == 14
    assert len(menu[EINSTELLUNGEN_SUBMENU_NAME]) == 2


def test_all_menu_items_have_valid_icon():
    menu = get_menu_list('Test_User')

    for main_menu_key in menu.keys():
        for menu_item in menu[main_menu_key]:
            print(menu_item)
            assert 'fa fa-' == menu_item['icon'][:len('fa fa-')]
