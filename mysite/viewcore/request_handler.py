'''
Created on 04.12.2017

@author: sebastian
'''
from flask import render_template
from flask import redirect
from mysite.test.RequestStubs import GetRequest
from mysite.viewcore import request_handler
from mysite.viewcore import viewcore
import random

DATABASE_VERSION = 0
SESSION_RANDOM = str(random.random())
REDIRECTOR = lambda x: redirect(x, code=301)
RENDER_FULL_FUNC = render_template
BASE_THEME_PATH = 'theme/'


def handle_request(request, request_action, html_base_page):
    if request.method == 'POST' and 'ID' in request.values:
        print('transactional request found')
        if request.values['ID'] != current_key():
            print('transaction rejected (requested:' + current_key() + ", got:" + request.values['ID'] + ')')
            context = viewcore.generate_base_context('Fehler')
            rendered_content = request_handler.request_handler.RENDER_FULL_FUNC(theme('error_race.html'), **{})
            context['content'] = rendered_content
            return request_handler.RENDER_FULL_FUNC(theme('index.html'), **context)
        print('transaction allowed')
        request_handler.DATABASE_VERSION = request_handler.DATABASE_VERSION + 1
        print('new db version: ' + str(request_handler.DATABASE_VERSION))

    context = request_action(request)
    viewcore.save_tainted()

    if request.method == 'POST' and 'redirect' in request.values:
        return request_handler.REDIRECTOR('/' + str(request.values['redirect']) + '/')

    if 'transaction_key' in context:
        context['ID'] = current_key()

    if '%Errortext' in context:
        rendered_content = context['%Errortext']
    else:
        rendered_content = request_handler.RENDER_FULL_FUNC(theme(html_base_page), **context)

    context['content'] = rendered_content
    response = request_handler.RENDER_FULL_FUNC(theme('index.html'), **context)
    return response

def theme(page):
    return request_handler.BASE_THEME_PATH + page

def current_key():
    return request_handler.SESSION_RANDOM + ' ' + viewcore.database_instance().name + '_VERSION_' + str(request_handler.DATABASE_VERSION)


def stub_me():
    request_handler.RENDER_FULL_FUNC = full_render_stub
    request_handler.REDIRECTOR = lambda x: x

def full_render_stub(theme, **context):
    return context

