from butler_offline.viewcore.context import generate_base_context, generate_transactional_context, \
    generate_redirect_context
from butler_offline.viewcore.context.builder import PageContext, TransactionalPageContext, RedirectPageContext
from butler_offline.viewcore.context import TRANSACTION_ID_KEY, REDIRECT_KEY


def test_migration_base_page_context():
    assert PageContext(pagename='my_page', database_name='my_database').as_dict() \
           == generate_base_context(pagename='my_page', database_name='my_database')


def test_migration_transactional_page_context():
    assert TransactionalPageContext(pagename='my_page', database_name='my_database').as_dict() \
           == generate_transactional_context('my_page', 'my_database')


def test_migration_redirect_page_context():
    assert RedirectPageContext(redirect_target_url='my_target', database_name='my_database', page_name='my_page')\
               .as_dict()\
           == generate_redirect_context('my_target')


def test_transaction_context_should_be_transactional_and_not_redirect():
    assert TransactionalPageContext(pagename='', database_name='').is_transactional()
    assert not TransactionalPageContext(pagename='', database_name='').is_redirect()


def test_base_context_should_not_be_transactional_and_redirect():
    assert not PageContext(pagename='', database_name='').is_transactional()
    assert not PageContext(pagename='', database_name='').is_redirect()


def test_redirect_context_should_be_redirect_and_not_transactional():
    assert RedirectPageContext(redirect_target_url='my_target', database_name='my_database', page_name='my_page')\
        .is_redirect()
    assert not RedirectPageContext(redirect_target_url='my_target', database_name='my_database', page_name='my_page')\
        .is_transactional()


def test_as_dict_with_transactional_context_should_contain_transaction_id():
    assert TRANSACTION_ID_KEY in TransactionalPageContext(pagename='', database_name='').as_dict()


def test_as_dict_with_base_context_should_not_contain_transaction_id():
    assert TRANSACTION_ID_KEY not in PageContext(pagename='', database_name='').as_dict()


def test_as_dict_redirect_context_should_contain_redirect_key():
    assert REDIRECT_KEY in RedirectPageContext(
        redirect_target_url='my_target',
        database_name='my_database',
        page_name='my_page')\
        .as_dict()

    assert RedirectPageContext(redirect_target_url='my_target', database_name='my_database', page_name='my_page')\
        .as_dict()[REDIRECT_KEY] == 'my_target'


def test_contains_with_not_contained_key_should_return_false():
    assert not PageContext(pagename='asdf', database_name='asdf').contains('asdf')


def test_contains_with_contained_key_should_return_true():
    context = PageContext(pagename="asdf", database_name="asdf")
    context.add('mykey', 'myvalue')
    assert context.contains('mykey')