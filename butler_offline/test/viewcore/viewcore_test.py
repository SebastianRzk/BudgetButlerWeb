import butler_offline.viewcore.menu
import butler_offline.viewcore.routes


def test_def_get_menu_list():
    menu_list = butler_offline.viewcore.menu.get_menu_list('')
    assert 'Persönliche Finanzen' in menu_list
    assert 'Gemeinsame Finanzen' in menu_list
    assert 'Sparen' in menu_list
    assert 'Einstellungen' in menu_list
