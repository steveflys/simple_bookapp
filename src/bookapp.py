# -*- coding: utf-8 -*-
import re

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    page = u"""
<h1>{title}</h1>
<table>
    <tr><th>Author</th><td>{author}</td></tr>
    <tr><th>Publisher</th><td>{publisher}</td></tr>
    <tr><th>ISBN</th><td>{isbn}</td></tr>
</table>
<a href="/">Back to the list</a>
"""
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    return page.format(**book)


def books():
    """return an html formatted list of books"""
    all_books = DB.titles()
    body = [u'<h1>My Bookshelf</h1>', '<ul>']
    item_template = u'<li><a href="/book/{id}">{title}</a></li>'
    for book in all_books:
        body.append(item_template.format(**book))
    body.append(u'</ul>')
    return u'\n'.join(body)


def resolve_path(path):
    """return a function and the args to call it with, if path is matched

    args may be an empty list
    func will be a callable

    if no path is matched, raise a NameError
    """
    urls = [(r'^$', books),
            (r'^book/(id[\d]+)$', book)]
    matchpath = path.lstrip('/')
    for regexp, func in urls:
        match = re.match(regexp, matchpath)
        if match is None:
            continue
        args = match.groups([])
        return func, args
    # we get here if no url matches
    raise NameError


def application(environ, start_response):
    headers = [("Content-type", "text/html; charset=utf8")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = u"<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = u"<h1>Internal Server Error</h1>"
    finally:
        encoded_body = body.encode('utf8')
        headers.append(('Content-length', str(len(encoded_body))))
        start_response(status, headers)
        return [encoded_body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
