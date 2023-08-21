from butler_offline.viewcore.context import generate_base_context, generate_redirect_context
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.context import ERROR_KEY
import logging
from typing import Self


class Message:
    def __init__(self, message_content: str):
        self._message_content = message_content

    def content(self) -> str:
        return self._message_content


class PageContext:
    def __init__(self, pagename: str, database_name: str):
        self._additional_context_values = {}
        self._basic_context_values = generate_base_context(pagename=pagename, database_name=database_name)
        self._error = False
        self._overwrite_page_to_render = False
        self._page_to_render = None
        self._error_text = None
        self._success_message = None
        self._error_message = None

    def overwrite_page_to_render(self, new_template_file: str):
        self._basic_context_values['special_page'] = new_template_file
        self._overwrite_page_to_render = True
        self._page_to_render = new_template_file

    def is_page_to_render_overwritten(self):
        return self._overwrite_page_to_render

    def page_to_render(self):
        return self._page_to_render

    def as_dict(self) -> dict:
        if self._error:
            self._additional_context_values[ERROR_KEY] = self._error_text
        return self._basic_context_values | self._additional_context_values

    def add(self, key: str, value) -> None:
        self._additional_context_values[key] = value

    def is_transactional(self) -> bool:
        return False

    def is_redirect(self) -> bool:
        return False

    def redirect_target_url(self) -> str | None:
        return None

    def get(self, key: str):
        return self._additional_context_values[key]

    def contains(self, key: str) -> bool:
        return key in self._additional_context_values

    def is_error(self) -> bool:
        return self._error

    def is_ok(self) -> bool:
        return not self._error

    def error_text(self) -> str | None:
        return self._error_text

    def throw_error(self, error_text: str) -> Self:
        self._error = True
        self._error_text = error_text
        return self

    def add_user_success_message(self, message: str) -> None:
        logging.info('SUCCESS: %s', message)
        self._success_message = Message(
            message_content=message
        )
        self._basic_context_values['message'] = True
        self._basic_context_values['message_type'] = 'success'
        self._basic_context_values['message_content'] = message.replace('\n', '<br>\n')

    def add_user_error_message(self, message: str) -> None:
        logging.error('ERROR: %s', message)
        self._error_message = Message(
            message_content=message
        )
        self._basic_context_values['message'] = True
        self._basic_context_values['message_type'] = 'error'
        self._basic_context_values['message_content'] = message.replace('\n', '<br>\n')

    def user_success_message(self) -> Message | None:
        return self._success_message

    def user_error_message(self) -> Message | None:
        return self._error_message


class TransactionalPageContext(PageContext):
    def __init__(self, pagename: str, database_name: str):
        super().__init__(pagename=pagename, database_name=database_name)
        self._transaction_context = {'ID': persisted_state.current_database_version()}

    def as_dict(self) -> dict:
        return super().as_dict() | self._transaction_context

    def is_transactional(self):
        return True


class RedirectPageContext(PageContext):
    def __init__(self, redirect_target_url: str, page_name: str, database_name: str):
        super().__init__(database_name=database_name, pagename=page_name)
        self._redirect_target_url = redirect_target_url

    def as_dict(self) -> dict:
        return generate_redirect_context(self._redirect_target_url)

    def is_redirect(self) -> bool:
        return True

    def redirect_target_url(self) -> str:
        return self._redirect_target_url


def generate_page_context(page_name: str) -> PageContext:
    return PageContext(pagename=page_name, database_name=persisted_state.database_instance().name)


def generate_transactional_page_context(page_name: str) -> TransactionalPageContext:
    return TransactionalPageContext(pagename=page_name, database_name=persisted_state.database_instance().name)


def generate_redirect_page_context(redirect_target_url: str) -> RedirectPageContext:
    return RedirectPageContext(redirect_target_url=redirect_target_url,
                               page_name='',
                               database_name=persisted_state.database_instance().name)
