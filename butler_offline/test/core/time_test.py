from butler_offline.core import time
from butler_offline.viewcore.converter import datum_from_german as datum
from datetime import datetime


def test_today_with_subbed_today_should_return_stubbed_date():
    time.stub_today_with(datum('01.01.2012'))
    assert time.today() == datum('01.01.2012')
    time.reset_viewcore_stubs()


def test_today_with_resetted_stub_should_return_today():
    time.stub_today_with(datum('01.01.2012'))
    time.reset_viewcore_stubs()
    assert time.today() == datetime.now().date()
    assert time.now().date() == datetime.now().date()
