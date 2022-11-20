
from flask import render_template
from flask import redirect
from requests.exceptions import ConnectionError

from butler_offline.viewcore import request_handler
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.base_html import set_error_message
from butler_offline.core.shares import shares_manager
from butler_offline.viewcore.state import persisted_state
import traceback
import logging

REDIRECTOR = lambda x: redirect(x, code=301)
RENDER_FULL_FUNC = render_template
BASE_THEME_PATH = 'theme/'

REDIRECT_KEY = 'redirect_to'


def handle_request(request, request_action, html_base_page):
    if request.method == 'POST' and 'ID' in request.values:
        logging.info('transactional request found')
        if request.values['ID'] != persisted_state.current_database_version():
            logging.info('transaction rejected (requested:' + persisted_state.current_database_version() + ", got:" + request.values['ID'] + ')')
            context = viewcore.generate_base_context('Fehler')
            rendered_content = request_handler.RENDER_FULL_FUNC(theme('core/error_race.html'), **{})
            context['content'] = rendered_content
            return request_handler.RENDER_FULL_FUNC(theme('index.html'), **context)
        logging.info('transaction allowed')
        persisted_state.increase_database_version()
        logging.info('new db version: ' + str(persisted_state.current_database_version()))

    context = viewcore.generate_base_context('Fehler')
    try:
        context = request_action(request)
        persisted_state.save_tainted()
    except ConnectionError as err:
        set_error_message(context, 'Verbindung zum Server konnte nicht aufgebaut werden.')
        context['%Errortext'] = ''
    except Exception as e:
        set_error_message(context, 'Ein Fehler ist aufgetreten: \n ' + str(e))
        logging.error(e)
        traceback.print_exc()
        context['%Errortext'] = ''
    shares_manager.save_if_needed(persisted_state.shares_data())


    if request.method == 'POST' and 'redirect' in request.values:
        return request_handler.REDIRECTOR('/' + str(request.values['redirect']) + '/')

    if '%Errortext' in context:
        rendered_content = context['%Errortext']
    elif REDIRECT_KEY in context:
        return REDIRECTOR(context[REDIRECT_KEY])
    else:
        if 'special_page' in context:
            html_base_page = context['special_page']
        rendered_content = request_handler.RENDER_FULL_FUNC(theme(html_base_page), **context)

    context['content'] = rendered_content
    response = request_handler.RENDER_FULL_FUNC(theme('index.html'), **context)
    return response


def create_redirect_context(url):
    return {
        REDIRECT_KEY: url
    }


def theme(page):
    return request_handler.BASE_THEME_PATH + page



def stub_me():
    request_handler.RENDER_FULL_FUNC = full_render_stub
    request_handler.REDIRECTOR = lambda x: x


def stub_me_theme():
    request_handler.RENDER_FULL_FUNC = full_render_stub_theme
    request_handler.REDIRECTOR = lambda x: x

def full_render_stub(theme, **context):
    return context


def full_render_stub_theme(theme, **context):
    if not 'content' in context:
        return theme
    return context
