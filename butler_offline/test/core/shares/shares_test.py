from butler_offline.core.shares import SharesInfo


def test_get_latest_data_for_with_empty_content():
    component_under_test = SharesInfo({})
    assert not component_under_test.get_latest_data_for('isin')


def test_get_latest_data_with_data():
    expected_data = {'test': 'data'}
    component_under_test = SharesInfo({})
    component_under_test.save('demoisin', 'demodate', 'demosource', expected_data)

    assert component_under_test.get_latest_data_for('demoisin') == expected_data


def test_get_last_changed_date_for_with_empty_content():
    component_under_test = SharesInfo({})
    assert not component_under_test.get_last_changed_date_for('isin')


def test_get_last_changed_date_with_data():
    component_under_test = SharesInfo({})
    component_under_test.save('demoisin', 'demodate', 'demosource', {'test': 'data'})

    assert component_under_test.get_last_changed_date_for('demoisin') == 'demodate'


def test_update_data():
    isin = 'demoisin'
    initial_data = {'test': 'data'}
    component_under_test = SharesInfo({})
    component_under_test.save(isin, 'demodate', 'demosource', initial_data)

    assert component_under_test.get_latest_data_for(isin) == initial_data

    updated_data = {'test': 'data-new'}
    component_under_test.save(isin, 'demodate', 'demosource', updated_data)

    assert component_under_test.get_latest_data_for(isin) == updated_data


def test_filter_out_isins_without_data():
    isin = 'demoisin'
    initial_data = {'test': 'data'}
    component_under_test = SharesInfo({})
    component_under_test.save(isin, 'demodate', 'demosource', initial_data)

    assert component_under_test.filter_out_isins_without_data(['demoisin', 'unknown']) == ['demoisin']

