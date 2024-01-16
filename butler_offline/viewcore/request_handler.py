import logging
from typing import Callable, TypeVar

from flask import Request

from butler_offline.core.database import Database
from butler_offline.core.shares import shares_manager
from butler_offline.viewcore.context import get_transaction_id, is_transactional_request
from butler_offline.viewcore.context.builder import PageContext
from butler_offline.viewcore.context.builder import generate_page_context
from butler_offline.viewcore.http import Redirector
from butler_offline.viewcore.http import Request as InternalRequest
from butler_offline.viewcore.page_executor import PageExecutor
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.state.persisted_state import CurrentDatabaseVersionProvider
from butler_offline.viewcore.template import Renderer


class WireThroughInterceptor:
    def __init__(self, handler):
        self._handler = handler

    def intercept(self, **varargs):
        return self._handler(**varargs)


TYPE_INPUT_CONTEXT = TypeVar("TYPE_INPUT_CONTEXT")
TYPE_INPUT_CONTEXT_CREATOR = Callable[[Database], TYPE_INPUT_CONTEXT]
TYPE_OUTPUT_PAGE_CONTEXT = TypeVar("TYPE_OUTPUT_PAGE_CONTEXT", bound=PageContext)
TYPE_USECASE = Callable[[InternalRequest, TYPE_INPUT_CONTEXT], TYPE_OUTPUT_PAGE_CONTEXT]


def handle(request: Request,
           context_creator: TYPE_INPUT_CONTEXT_CREATOR,
           handle_function: TYPE_USECASE,
           html_base_page: str,
           renderer: Renderer = Renderer(),
           redirector: Redirector = Redirector(),
           page_executor: PageExecutor = PageExecutor(),
           current_database_version_provider: CurrentDatabaseVersionProvider = CurrentDatabaseVersionProvider()
           ):
    return REQUEST_HANDLER_INTERCEPTOR.intercept(request=request,
                                                 request_action=handle_function,
                                                 context_creator=context_creator,
                                                 html_base_page=html_base_page,
                                                 renderer=renderer,
                                                 page_executor=page_executor,
                                                 redirector=redirector,
                                                 current_database_version_provider=current_database_version_provider
                                                 )


def handle_for_context_created(
        request: InternalRequest,
        context: PageContext,
        html_base_page: str,
        renderer: Renderer = Renderer(),
        redirector: Redirector = Redirector(),
        current_database_version_provider: CurrentDatabaseVersionProvider = CurrentDatabaseVersionProvider(),
        overwrite_taint_mode: bool = False
    ):
    database = persisted_state.database_instance()
    if context.is_ok():
        if database.is_tainted():
            if not is_transactional_request(request) and not overwrite_taint_mode:
                raise ModificationWithoutTransactionContext()
            persisted_state.save_tainted()

    shares_manager.save_if_needed(persisted_state.shares_data())

    if context.is_error():
        rendered_content = context.error_text()
    elif context.is_redirect():
        return redirector.temporary_redirect(context.redirect_target_url())
    else:
        if context.is_page_to_render_overwritten():
            html_base_page = context.page_to_render()
        page_context = context.get_page_context_map()
        if context.is_transactional():
            page_context['ID'] = current_database_version_provider.current_database_version()
        rendered_content = renderer.render(
            html=html_base_page,
            **page_context)

    return renderer.render(
        html='index.html',
        **context.generate_basic_page_context(
            inner_page=rendered_content,
            database_name=database.name
        )
    )


def __handle_request(
        request: Request,
        request_action: TYPE_USECASE,
        context_creator: TYPE_INPUT_CONTEXT_CREATOR,
        html_base_page: str,
        renderer: Renderer,
        page_executor: PageExecutor,
        redirector: Redirector,
        current_database_version_provider: CurrentDatabaseVersionProvider
):
    database = persisted_state.database_instance()
    request = create_internal_request(request)
    if is_transactional_request(request):
        logging.info('transactional request found')
        transaction_id = get_transaction_id(request)
        if transaction_id != persisted_state.current_database_version():
            logging.error(
                'transaction rejected (requested:' +
                current_database_version_provider.current_database_version() +
                ", got:" +
                transaction_id + ')')
            return handle_transaction_out_of_sync(
                renderer=renderer,
                database_name=database.name
            )
        logging.info('transaction allowed')
        persisted_state.increase_database_version()
        logging.info('new db version: ' + str(persisted_state.current_database_version()))

    input_context = context_creator(database)
    context = page_executor.execute(page_handler=request_action, request=request, context=input_context)

    return handle_for_context_created(context=context,
                                      redirector=redirector,
                                      html_base_page=html_base_page,
                                      request=request,
                                      renderer=renderer)


REQUEST_HANDLER_INTERCEPTOR = WireThroughInterceptor(handler=__handle_request)


def create_internal_request(request: Request) -> InternalRequest:
    return InternalRequest(
        values=request.values.copy(),
        args=request.args.copy(),
        method=request.method
    )


def handle_transaction_out_of_sync(
        renderer: Renderer,
        database_name: str,
):
    context = generate_page_context('Fehler')
    rendered_content = renderer.render('core/error_race.html', **{})
    return renderer.render('index.html', **context.generate_basic_page_context(
        inner_page=rendered_content,
        database_name=database_name,
    ))


class ModificationWithoutTransactionContext(Exception):
    pass
