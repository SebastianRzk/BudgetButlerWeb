from pandas import DataFrame
from butler_offline.core.database import Database


def test_frame_to_list_of_dicts_with_empty_dataframe_should_return_empty_list():
    empty_dataframe = DataFrame()

    result = Database('test_database').frame_to_list_of_dicts(empty_dataframe)

    assert result == []


def test_frame_to_list_of_dicts_with_dataframe_should_return_list_of_dicts():
    dataframe = DataFrame([{'col1': 'test1', 'col2': 1}, {'col1': 'test2', 'col2': 2}])

    result = Database('test_database').frame_to_list_of_dicts(dataframe)

    assert len(result) == 2
    assert result[0]['col1'] == 'test1'
    assert result[0]['col2'] == 1
    assert result[1]['col1'] == 'test2'
    assert result[1]['col2'] == 2
