from butler_offline.core.shares.shares_manager import load_data, save_if_needed, SHARES_PATH
from butler_offline.core import file_system
from butler_offline.core.shares import SharesInfo
from butler_offline.test.core.file_system_stub import FileSystemStub


def test_load_data_empty():
    file_system.INSTANCE = FileSystemStub()

    result = load_data()

    assert not result.content


def test_load_data_filled():
    file_system.INSTANCE = FileSystemStub()
    file_system.instance().write(SHARES_PATH, '{"demo": 1234}')

    result = load_data()

    assert result.content == {'demo': 1234}


def test_save_if_needed_with_no_changes():
    file_system.INSTANCE = FileSystemStub()

    save_if_needed(SharesInfo({}))

    assert not file_system.INSTANCE.get_interaction_count()


def test_save_if_needed():
    file_system.INSTANCE = FileSystemStub()
    shares_info = SharesInfo({})
    shares_info.save('isin', '2021-01-01', 'test_data', {'demo': 'data'})

    save_if_needed(shares_info)

    assert file_system.INSTANCE.read(SHARES_PATH) == [
        '{"isin": {"data": [{"date": "2021-01-01", "data": {"demo": "data"}, "source": "test_data"}]}}']


