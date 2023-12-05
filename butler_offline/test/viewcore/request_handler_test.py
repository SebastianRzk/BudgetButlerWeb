from requests.exceptions import ConnectionError

from butler_offline.core import file_system
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.viewcore.request_handler import RedirectorStub, RendererStub
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_redirect_page_context, generate_page_context, PageContext


def set_up():
    file_system.INSTANCE = FileSystemStub()


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
        context_creator=lambda db: EmptyContext(),
        redirector=RedirectorStub()
    )
    assert result == 'to: to_url'


def index_generate_extra_page(request, context: EmptyContext):
    context = generate_page_context('asdf')
    context.overwrite_page_to_render(new_template_file='something_special', new_title='new title')
    return context


def test_extra_page():
    renderer = RendererStub()

    request_handler.handle(
        request=GetRequest(),
        html_base_page='something_normal',
        context_creator=lambda db: EmptyContext(),
        handle_function=index_generate_extra_page,
        renderer=renderer
    )

    assert renderer.result().html_pages_requested_to_render() == ['something_special']
    assert renderer.get_index_content()['element_titel'] == 'new title'


def index_generate_normal_page(request, context: EmptyContext):
    return generate_page_context('something_normal')


def test_default_page():
    renderer = RendererStub()
    request_handler.handle(
        request=GetRequest(),
        html_base_page='something_normal',
        handle_function=index_generate_normal_page,
        context_creator=lambda db: EmptyContext(),
        renderer=renderer
    )
    assert renderer.result().html_pages_requested_to_render() == ['something_normal']


def index_raise_exception(request, context: EmptyContext) -> PageContext:
    raise Exception()


def index_raise_http_error(request, context: EmptyContext) -> PageContext:
    raise ConnectionError()


def test_http_exception():
    renderer = RendererStub()

    result = request_handler.handle(
        request=GetRequest(),
        html_base_page='something_normal',
        handle_function=index_raise_http_error,
        context_creator=lambda db: EmptyContext(),
        renderer=renderer
    )

    assert renderer.result().html_pages_requested_to_render() == []
    result = renderer.get_index_content()
    assert result['content'] == 'Verbindung zum Server konnte nicht aufgebaut werden.'


def test_exception():
    renderer = RendererStub()
    request_handler.handle(
        request=GetRequest(),
        handle_function=index_raise_exception,
        html_base_page='something_normal',
        context_creator=lambda db: EmptyContext(),
        renderer=renderer
    )
    assert renderer.result().html_pages_requested_to_render() == []
    result = renderer.get_index_content()
    assert result['content'] == 'Ein Fehler ist aufgetreten: \n '
