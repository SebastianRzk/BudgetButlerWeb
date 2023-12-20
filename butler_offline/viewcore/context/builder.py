import logging
from typing import Self

from butler_offline.viewcore.context import generate_base_context
from butler_offline.viewcore.menu import get_name_from_key


class VorgeschlageneProblembehebung:
    def __init__(self, link: str, link_beschreibung: str):
        self._link = link
        self._link_beschreibung = link_beschreibung

    def link(self) -> str:
        return self._link

    def link_beschreibung(self) -> str:
        return self._link_beschreibung


class Message:
    def __init__(self, message_content: str,
                 vorgeschlagene_problembehebungen: list[VorgeschlageneProblembehebung] | None = None):
        self._message_content = message_content
        if not vorgeschlagene_problembehebungen:
            _vorgeschlagene_problembehebungen = []
        self._vorgeschlagene_problembehebungen = vorgeschlagene_problembehebungen

    def content(self) -> str:
        return self._message_content

    def vorgeschlagene_problembehebungen(self) -> list[VorgeschlageneProblembehebung]:
        return self._vorgeschlagene_problembehebungen


class PageContext:
    def __init__(self, pagename: str):
        self._pagename = pagename
        self._additional_context_values = {}
        self._error = False
        self._overwrite_page_to_render = False
        self._page_to_render = None
        self._error_text = None
        self._success_message: Message | None = None
        self._error_message: Message | None = None
        self._info_messages: list[Message] = []
        self._new_page_title: str | None = None

    def overwrite_page_to_render(self, new_template_file: str, new_title: str):
        self._overwrite_page_to_render = True
        self._page_to_render = new_template_file
        self._new_page_title = new_title

    def overwrite_page_titel(self, new_title: str):
        self._new_page_title = new_title

    def is_page_to_render_overwritten(self):
        return self._overwrite_page_to_render

    def page_to_render(self):
        return self._page_to_render

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

    def get_page_context_map(self) -> dict:
        if self._new_page_title:
            self._additional_context_values['element_titel'] = self._new_page_title
        else:
            self._additional_context_values['element_titel'] = get_name_from_key(self._pagename)
        return self._additional_context_values

    def generate_basic_page_context(self, inner_page: str, database_name: str) -> dict:
        basic_context = generate_base_context(pagename=self._pagename, database_name=database_name)
        basic_context['content'] = inner_page
        if self.user_success_message():
            basic_context['message'] = True
            basic_context['message_type'] = 'success'
            basic_context['message_content'] = self._success_message.content().replace('\n', '<br>\n')

        if self.user_error_message():
            basic_context['message'] = True
            basic_context['message_type'] = 'error'
            basic_context['message_content'] = self._error_message.content().replace('\n', '<br>\n')

        basic_context['info_messages'] = self._info_messages

        if self._new_page_title:
            basic_context['element_titel'] = self._new_page_title
        return basic_context

    def add_user_success_message(self, message: str) -> None:
        logging.info('SUCCESS: %s', message)
        self._success_message = Message(
            message_content=message
        )

    def add_user_error_message(self, message: str) -> None:
        logging.error('ERROR: %s', message)
        self._error_message = Message(
            message_content=message
        )

    def add_info_message(self, message: str,
                         vorgeschlagene_problembehebungen: list[VorgeschlageneProblembehebung] | None) -> None:
        logging.info('INFO: %s', message)
        self._info_messages.append(Message(
            message_content=message,
            vorgeschlagene_problembehebungen=vorgeschlagene_problembehebungen
        ))

    def get_info_messages(self) -> list[Message]:
        return self._info_messages

    def user_success_message(self) -> Message | None:
        return self._success_message

    def user_error_message(self) -> Message | None:
        return self._error_message

    def pagename(self) -> str:
        return self._pagename


class TransactionalPageContext(PageContext):
    def __init__(self, pagename: str):
        super().__init__(pagename=pagename)

    def is_transactional(self):
        return True


class RedirectPageContext(PageContext):
    def __init__(self, redirect_target_url: str, page_name: str):
        super().__init__(pagename=page_name)
        self._redirect_target_url = redirect_target_url

    def is_redirect(self) -> bool:
        return True

    def redirect_target_url(self) -> str:
        return self._redirect_target_url


def generate_page_context(page_name: str) -> PageContext:
    return PageContext(pagename=page_name)


def generate_transactional_page_context(page_name: str) -> TransactionalPageContext:
    return TransactionalPageContext(pagename=page_name)


def generate_redirect_page_context(redirect_target_url: str) -> RedirectPageContext:
    return RedirectPageContext(redirect_target_url=redirect_target_url,
                               page_name='')
