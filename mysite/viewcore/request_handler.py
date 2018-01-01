'''
Created on 04.12.2017

@author: sebastian
'''
from django.template.loader import render_to_string
from django.shortcuts import render
from test.RequestStubs import GetRequest
from viewcore import request_handler
from viewcore import viewcore
import random

DATABASE_VERSION = 0
SESSION_RANDOM = str(random.random())
RENDER_PARTIALLY_FUNC = render_to_string
RENDER_FULL_FUNC = render


def handle_request(request, request_action, html_base_page):
    if request.method == 'POST' and 'ID' in request.POST:
        print('transactional request found')
        if request.POST['ID'] != current_key():
            print('transaction rejected (requested:' + current_key() + ", got:" + request.POST['ID'] + ')')
            context = viewcore.generate_base_context('Fehler')
            rendered_content = request_handler.request_handler.RENDER_PARTIALLY_FUNC('theme/error_race.html', {}, request=request)
            context['content'] = rendered_content
            return request_handler.RENDER_FULL_FUNC(request, 'theme/index.html', context)
        print('transaction allowed')
        request_handler.DATABASE_VERSION = request_handler.DATABASE_VERSION + 1
        print('new db version: ' + str(request_handler.DATABASE_VERSION))

    context = request_action(request)

    if 'transaction_key' in context:
        context['ID'] = current_key()

    if '%Errortext' in context:
        rendered_content = context['%Errortext']
    else:
        rendered_content = request_handler.RENDER_PARTIALLY_FUNC(html_base_page, context, request=request)

    context['content'] = rendered_content
    response = request_handler.RENDER_FULL_FUNC(request, 'theme/index.html', context)
    print('Page generated')
    return response

def current_key():
    return request_handler.SESSION_RANDOM + ' ' + viewcore.database_instance().name + '_VERSION_' + str(request_handler.DATABASE_VERSION)

def stub_me():
    request_handler.RENDER_PARTIALLY_FUNC = partially_render_stub
    request_handler.RENDER_FULL_FUNC = full_render_stub

def partially_render_stub(html_base_page, context, request):
    return html_base_page

def full_render_stub(request, theme, context):
    return context

