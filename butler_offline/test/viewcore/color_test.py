from butler_offline.viewcore.colors import GenericDesignColorChooser


def test_generic_color_chooser():
    chooser = GenericDesignColorChooser(colors=['r', 'g'], values=['1', '2', '3'])

    assert chooser.get_for_value('1') == '#r'
    assert chooser.get_for_value('2') == '#g'
    assert chooser.get_for_value('3') == '#r'
