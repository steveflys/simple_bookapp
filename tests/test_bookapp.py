# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest


# Tests of the book database itself
def test_all_titles_returned(database, storage):
    actual_titles = database.titles()
    assert len(actual_titles) == len(storage)


def test_all_titles_correct(database, storage):
    actual_titles = database.titles()
    for actual_title in actual_titles:
        assert actual_title['id'] in storage
        actual = actual_title['title']
        expected = storage[actual_title['id']]['title']
        assert actual == expected


def test_title_info_complete(database, storage):
    for use_id, expected in storage.items():
        actual = database.title_info(use_id)
        # demonstrate all actual keys are expected
        for key in actual:
            assert key in expected
        # demonstrate all expected keys are present in actual
        for key in expected:
            assert key in actual


def test_title_info_correct(database, storage):
    for book_id, expected in storage.items():
        actual = database.title_info(book_id)
        assert actual == expected


# Tests of the dispatch function
def test_root_returns_books_function():
    """verify that the correct function is returned by the root path"""
    from bookapp import resolve_path
    from bookapp import books as expected
    path = '/'
    actual, args = resolve_path(path)
    assert actual is expected


def test_root_returns_no_args():
    """verify that no args are returned for the root path"""
    from bookapp import resolve_path
    path = '/'
    func, actual = resolve_path(path)
    assert not actual


def test_book_path_returns_book_function(storage):
    """verify that the correct function is returned by the book path"""
    from bookapp import resolve_path
    from bookapp import book as expected
    for book_id in storage.keys():
        path = '/book/{0}'.format(book_id)
        actual, args = resolve_path(path)
        assert actual is expected


def test_book_path_returns_bookid_in_args(storage):
    from bookapp import resolve_path
    for expected in storage.keys():
        path = '/book/{0}'.format(expected)
        func, actual = resolve_path(path)
        assert expected in actual


def test_bad_path_raises_name_error():
    """verify that the correct error is raised for a bad path"""
    from bookapp import resolve_path
    path = '/not/valid/path'
    with pytest.raises(NameError):
        resolve_path(path)


# Tests of the `books' function
def test_all_book_titles_in_result(storage):
    """verify book titles appear in listing page"""
    from bookapp import books
    actual = books()
    for book_id, info in storage.items():
        expected = info['title']
        assert expected in actual


def test_all_book_ids_in_result(storage):
    """verify book ids appear in listing page"""
    from bookapp import books
    actual = books()
    for expected in storage:
        assert expected in actual


# Tests of the 'book' function
def test_all_ids_have_results(storage):
    """verify that all stored ids can be resolved to pages"""
    from bookapp import book
    for book_id in storage:
        actual = book(book_id)
        assert actual


def test_id_returns_correct_results(storage):
    """verify that the correct book page is built by the book function"""
    from bookapp import book
    for book_id, book_info in storage.items():
        actual = book(book_id)
        for expected in book_info.values():
            assert expected in actual


def test_bad_id_raises_name_error():
    """verify that a bad book id will raise the expected NameError"""
    from bookapp import book
    bad_id = "sponge"
    with pytest.raises(NameError):
        book(bad_id)


# Functional Tests
def test_listing_page_links(app, storage):
    """verify that the homepage contains links to all books"""
    response = app.get('/', status=200)
    actual = response.html
    for book_id, book_data in storage.items():
        expected_title = book_data['title']
        expected_path = "/book/{}".format(book_id)
        link = actual.find('a', href=expected_path)
        assert link and expected_title in link


def test_book_page_titles(app, storage):
    for book_id, book_data in storage.items():
        path = "/book/{}".format(book_id)
        html = app.get(path, status=200).html
        expected_title = book_data['title']
        actual_title = html.find('h1')
        assert expected_title in actual_title


def test_bad_path_returns_404(app):
    """assert that a bad path returns 404"""
    assert app.get('/not/a/path', status=404)


def test_bad_book_id_returns_404(app):
    """assert that a bad book id will raise 404 for books"""
    bad_path = "/book/id1000000"
    assert app.get(bad_path, status=404)
