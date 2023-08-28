from butler_offline.viewcore.context.builder import PageContext, TransactionalPageContext, RedirectPageContext


def test_transaction_context_should_be_transactional_and_not_redirect():
    assert TransactionalPageContext(pagename='').is_transactional()
    assert not TransactionalPageContext(pagename='').is_redirect()


def test_base_context_should_not_be_transactional_and_redirect():
    assert not PageContext(pagename='').is_transactional()
    assert not PageContext(pagename='').is_redirect()


def test_redirect_context_should_be_redirect_and_not_transactional():
    assert RedirectPageContext(redirect_target_url='my_target', page_name='my_page')\
        .is_redirect()
    assert not RedirectPageContext(redirect_target_url='my_target', page_name='my_page')\
        .is_transactional()


def test_contains_with_not_contained_key_should_return_false():
    assert not PageContext(pagename='asdf').contains('asdf')


def test_contains_with_contained_key_should_return_true():
    context = PageContext(pagename='asdf')
    context.add('mykey', 'myvalue')
    assert context.contains('mykey')


def test_page_context_without_error_should_return_no_error():
    context = PageContext(pagename="")
    assert not context.is_error()
    assert not context.error_text()


def test_page_context_with_error_should_return_error():
    context = PageContext(pagename="")
    context.throw_error("something went wrong")

    assert context.is_error()
    assert context.error_text() == "something went wrong"
