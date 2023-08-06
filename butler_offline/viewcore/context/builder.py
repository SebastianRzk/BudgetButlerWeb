from butler_offline.viewcore.context import generate_base_context, generate_redirect_context
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.context import ERROR_KEY
from typing import Self


class PageContext:
    def __init__(self, pagename: str, database_name: str):
        self._additional_context_values = {}
        self._basic_context_values = generate_base_context(pagename=pagename, database_name=database_name)
        self._error = False
        self._error_text = None

    def as_dict(self) -> dict:
        if self._error:
            self._additional_context_values[ERROR_KEY] = self._error_text

        return self._basic_context_values | self._additional_context_values

    def add(self, key: str, value):
        self._additional_context_values[key] = value

    def is_transactional(self):
        return False

    def is_redirect(self) -> bool:
        return False

    def redirect_target_url(self) -> str | None:
        return None

    def get(self, key: str):
        return self._additional_context_values[key]

    def contains(self, key: str):
        return key in self._additional_context_values

    def is_error(self):
        return self._error

    def error_text(self):
        return self._error_text

    def throw_error(self, error_text: str) -> Self:
        self._error = True
        self._error_text = error_text
        return self


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
