
from flask import redirect
from requests.exceptions import ConnectionError

from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context import generate_base_context, REDIRECT_KEY
from butler_offline.viewcore.base_html import set_error_message
from butler_offline.core.shares import shares_manager
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.context import get_transaction_id, is_transactional_request, ERROR_KEY, is_error
import traceback
import logging
from butler_offline.viewcore import template
from butler_offline.viewcore.template import renderer_instance

REDIRECTOR = lambda x: redirect(x, code=301)



def handle_request(request, request_action, html_base_page):
    if is_transactional_request(request):
        logging.info('transactional request found')
        transaction_id = get_transaction_id(request)
        if transaction_id != persisted_state.current_database_version():
            return handle_transaction_out_of_sync(transaction_id)
        logging.info('transaction allowed')
        persisted_state.increase_database_version()
        logging.info('new db version: ' + str(persisted_state.current_database_version()))

    context = take_action(request, request_action)

    if not is_error(context):
        if persisted_state.database_instance().is_tainted():
            if not is_transactional_request(request):
                raise ModificationWithoutTransactionContext()
            persisted_state.save_tainted()

    shares_manager.save_if_needed(persisted_state.shares_data())

    if is_error(context):
        rendered_content = context[ERROR_KEY]
    elif REDIRECT_KEY in context:
        return REDIRECTOR(context[REDIRECT_KEY])
    else:
        if 'special_page' in context:
            html_base_page = context['special_page']
        rendered_content = renderer_instance().render(html_base_page, **context)

    context['content'] = rendered_content
    response = renderer_instance().render('index.html', **context)
    return response


def handle_transaction_out_of_sync(transaction_id):
    logging.error(
        'transaction rejected (requested:' + persisted_state.current_database_version() + ", got:" + transaction_id + ')')
    context = generate_base_context('Fehler')
    rendered_content = renderer_instance().render('core/error_race.html', **{})
    context['content'] = rendered_content
    return renderer_instance().render('index.html', **context)


def take_action(request, request_action):
    context = generate_base_context('Fehler')
    try:
        context = request_action(request)
    except ConnectionError as err:
        set_error_message(context, 'Verbindung zum Server konnte nicht aufgebaut werden.')
        context[ERROR_KEY] = ''
    except Exception as e:
        set_error_message(context, 'Ein Fehler ist aufgetreten: \n ' + str(e))
        logging.error(e)
        traceback.print_exc()
        context[ERROR_KEY] = ''
    return context




def stub_me():
    template.RENDERER = RendererStub()
    request_handler.REDIRECTOR = lambda x: x


def stub_me_theme():
    template.RENDERER = RendererThemeStub()
    request_handler.REDIRECTOR = lambda x: x


class RendererStub():
    def render(self, template, **context):
        return context


class RendererThemeStub():
    def render(self, template, **context):
        if not 'content' in context:
            return template
        return context


class ModificationWithoutTransactionContext(Exception):
    pass
