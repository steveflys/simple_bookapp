# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
import webtest


@pytest.fixture(scope='session')
def database():
    from bookdb import BookDB
    return BookDB()


@pytest.fixture(scope='session')
def storage():
    from bookdb import database
    return database


@pytest.fixture()
def app():
    from bookapp import application
    app = webtest.TestApp(application)
    return app
