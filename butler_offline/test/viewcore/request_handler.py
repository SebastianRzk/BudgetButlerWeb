from typing import Callable
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import persisted_state
from butler_offline.core.database import Database


class TestRequestHandlerResult:

    def __init__(self, number_of_calls, html_pages):
        self._number_of_calls = number_of_calls
        self._html_pages = html_pages

    def number_of_calls(self) -> int:
        return self._number_of_calls

    def html_pages_requested_to_render(self) -> dict[str]:
        return self._html_pages


class TestRequestHandler:
    _number_of_calls = 0
    _html_pages = []

    def __init__(self):
        self._number_of_calls = 0
        self._html_pages = []

    def request_handler_stub(self) -> Callable:
        def handler(request, request_action, html_base_page):
            self._html_pages.append(html_base_page)
            self._number_of_calls += 1
            return {}
        return handler

    def result(self) -> TestRequestHandlerResult:
        return TestRequestHandlerResult(number_of_calls=self._number_of_calls, html_pages=self._html_pages)


def run_in_mocked_handler(index_handle: Callable) -> TestRequestHandlerResult:
    database_backup = persisted_state.DATABASE_INSTANCE
    persisted_state.DATABASE_INSTANCE = Database()

    request_handler_function_original = request_handler.REQUEST_HANDLER
    request_handler_stub = TestRequestHandler()
    request_handler.REQUEST_HANDLER = request_handler_stub.request_handler_stub()

    index_handle()

    request_handler.REQUEST_HANDLER = request_handler_function_original
    persisted_state.DATABASE_INSTANCE = database_backup
    return request_handler_stub.result()
