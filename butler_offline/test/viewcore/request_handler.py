from typing import Callable

from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import PageContext
from butler_offline.viewcore.http import Redirector
from butler_offline.viewcore.page_executor import PageExecutor
from butler_offline.viewcore.state.persisted_state import CurrentDatabaseVersionProvider
from butler_offline.viewcore.template import Renderer
from butler_offline.core import file_system
from butler_offline.test.core import file_system_stub


class TestRequestHandlerResult:

    def __init__(self, number_of_calls, html_pages):
        self._number_of_calls = number_of_calls
        self._html_pages = html_pages

    def number_of_calls(self) -> int:
        return self._number_of_calls

    def html_pages_requested_to_render(self) -> dict[str]:
        return self._html_pages


class RendererStub(Renderer):
    _number_of_calls = 0
    _html_pages = []
    _context = {}

    def __init__(self):
        super().__init__()
        self._number_of_calls = 0
        self._html_pages = []

    def render(self, html, **context):
        self._context[html] = context
        if html == 'index.html':
            return
        self._html_pages.append(html)
        self._number_of_calls += 1

    def result(self) -> TestRequestHandlerResult:
        return TestRequestHandlerResult(number_of_calls=self._number_of_calls, html_pages=self._html_pages)

    def get_context_for(self, html: str):
        return self._context[html]

    def get_index_content(self):
        return self.get_context_for('index.html')


class InterceptorWrapper(request_handler.WireThroughInterceptor):
    def __init__(self, handler: request_handler.WireThroughInterceptor, replacement: dict):
        super().__init__(handler=None)
        self._handler = handler
        self._replacement = replacement

    def intercept(self, **varargs):
        varargs.update(self._replacement)
        return self._handler.intercept(**varargs)


class RedirectorStub(Redirector):
    def __init__(self):
        super().__init__()

    def temporary_redirect(self, destination: str):
        return 'to: ' + destination


class PageExecutorStub(PageExecutor):
    def __init__(self):
        super().__init__()

    def execute(self,
                page_handler,
                request,
                context) -> PageContext:
        return PageContext('stub page name')


class DatabaseVersionProviderStub(CurrentDatabaseVersionProvider):
    def __init__(self):
        super().__init__()

    def current_database_version(self) -> str:
        return 'stubbed database version'


def run_in_mocked_handler(index_handle: Callable) -> TestRequestHandlerResult:
    request_handler_function_original = request_handler.REQUEST_HANDLER_INTERCEPTOR
    file_system_original = file_system.INSTANCE
    file_system.INSTANCE = file_system_stub.FileSystemStub()
    renderer = RendererStub()
    request_handler.REQUEST_HANDLER_INTERCEPTOR = InterceptorWrapper(
        handler=request_handler_function_original,
        replacement={
            'renderer': renderer,
            'redirector': RedirectorStub(),
            'page_executor': PageExecutorStub(),
            'current_database_version_provider': DatabaseVersionProviderStub()
        }
    )
    index_handle()

    request_handler.REQUEST_HANDLER_INTERCEPTOR = request_handler_function_original
    file_system.INSTANCE = file_system_original

    return renderer.result()
