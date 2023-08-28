from typing import Callable, TypeVar
from requests.exceptions import ConnectionError

from flask import Request
import logging

from butler_offline.viewcore.context.builder import PageContext
from butler_offline.viewcore.context.builder import generate_page_context

TYPE_INPUT_CONTEXT = TypeVar("TYPE_INPUT_CONTEXT")


class PageExecutor:
    def execute(self,
                page_handler: Callable[[Request, TYPE_INPUT_CONTEXT], PageContext],
                request: Request,
                context: TYPE_INPUT_CONTEXT) -> PageContext:

        result_context = generate_page_context('Fehler')

        try:
            return page_handler(request, context)
        except ConnectionError as _:
            return result_context.throw_error('Verbindung zum Server konnte nicht aufgebaut werden.')
        except Exception as e:
            logging.error(e)
            return result_context.throw_error('Ein Fehler ist aufgetreten: \n ' + str(e))

