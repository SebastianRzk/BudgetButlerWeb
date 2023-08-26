from requests.exceptions import ConnectionError
from butler_offline.viewcore.context.builder import generate_redirect_page_context, generate_page_context, PageContext
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.core import file_system


def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    persisted_state.database_instance()
    request_handler.stub_me_theme()


class EmptyContext:
    pass


def index_make_redirect(request, context: EmptyContext):
    return generate_redirect_page_context('to_url')


def test_manual_redirect():
    set_up()
    result = request_handler.handle(
        request=GetRequest(),
        handle_function=index_make_redirect,
        html_base_page='nothing',
        context_creator=lambda db: EmptyContext()
    )
    assert result == 'to_url'


def index_generate_extra_page(request, context: EmptyContext):
    context = generate_page_context('asdf')
    context.overwrite_page_to_render('something_special')
    return context


def test_extra_page():
    set_up()

    result = request_handler.handle(
        request=GetRequest(),
        html_base_page='something_normal',
        context_creator=lambda db: EmptyContext(),
        handle_function=index_generate_extra_page
    )
    assert result['content'] == 'something_special'


def index_generate_normal_page(request, context: EmptyContext):
    return generate_page_context('something_normal')


def test_default_page():
    set_up()
    result = request_handler.handle(
        request=GetRequest(),
        html_base_page='something_normal',
        handle_function=index_generate_normal_page,
        context_creator=lambda db: EmptyContext()
    )
    assert result['content'] == 'something_normal'


def index_raise_exception(request, context: EmptyContext) -> PageContext:
    raise Exception()


def index_raise_http_error(request, context: EmptyContext) -> PageContext:
    raise ConnectionError()


def test_http_exception():
    set_up()
    request_handler.stub_me()

    result = request_handler.handle(
        request=GetRequest(),
        html_base_page='something_normal',
        handle_function=index_raise_http_error,
        context_creator=lambda db: EmptyContext()
    )
    assert result['message']
    assert result['message_type'] == 'error'
    assert result['message_content'] == 'Verbindung zum Server konnte nicht aufgebaut werden.'


def test_exception():
    set_up()
    request_handler.stub_me()

    result = request_handler.handle(
        request=GetRequest(),
        handle_function=index_raise_exception,
        html_base_page='something_normal',
        context_creator=lambda db: EmptyContext()
    )
    assert result['message']
    assert result['message_type'] == 'error'
    assert result['message_content'] == 'Ein Fehler ist aufgetreten: <br>\n '
