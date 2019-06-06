import pytest
from db import StatDataBase
from main import get_vk_subs
import requests


class MockResponse:

    @staticmethod
    def json():
        return {'response': {'count': 1111111, 'items': [348, 485]}}


class MockWrongResponse:

    @staticmethod
    def json():
        return {'Error!': 'There are no subs and wrong format!!!'}


@pytest.fixture()
def setup():
    db = StatDataBase(':memory:')
    return db


@pytest.fixture()
def setup_full_db():
    db = StatDataBase(':memory:')
    db.db_init()
    return db


@pytest.fixture()
def setup_db_with_group():
    db = StatDataBase(':memory:')
    db.db_init()
    db.db_insert_group('test_group')
    return db


# протестировать фукнцию get_vk_subs, мокая ответ API


def test_get_vk_subs(setup_full_db, monkeypatch):
    db = setup_full_db

    def mock_get(*args, **kwargs):
        return MockResponse()

    def wrong_mock_get(*args, **kwargs):
        return MockWrongResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    assert get_vk_subs('test_fake_group') == 1111111
    monkeypatch.setattr(requests, "get", wrong_mock_get)
    assert get_vk_subs('test_fake_group') == 0
    # assert get_vk_subs('rambler') > 1
    # assert get_vk_subs('test_fake_group_without_subs') == 0


# протестировать корректность использования API


def test_get_subs(setup_full_db):
    db = setup_full_db
    assert get_vk_subs('rambler') > 1
    assert get_vk_subs('test_fake_group_without_subs') == 0


def test_db_init(setup):
    db = setup
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='social_group';")
    assert db.cursor.fetchone() is None
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='subs_stat';")
    assert db.cursor.fetchone() is None
    db.db_init()
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='social_group';")
    assert 'social_group' in db.cursor.fetchone()
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='subs_stat';")
    assert 'subs_stat' in db.cursor.fetchone()


# проветирвоать db_insert_group (Селектим группу, которой нет, затем добавляем группу в БД и селектим её)


def test_db_insert_group(setup_full_db):
    db = setup_full_db
    db.cursor.execute("SELECT count(*) FROM social_group;")
    assert db.cursor.fetchone()[0] == 0
    db.db_insert_group('test_group')
    db.cursor.execute("SELECT * FROM social_group;")
    assert db.cursor.fetchone() == (1, 'test_group')


# проверить db_check_group (чекаем группу, которой нет, чекаем группу, которая есть)


def test_db_check_group(setup_db_with_group):
    db = setup_db_with_group
    assert db.db_check_group('test_group') == 1
    assert db.db_check_group('fake_group') == 0


# проверить db_insert_subs (проверяем, что записи по группе нет, добавляем запись и проверяем, что появились данные)


def test_db_insert_subs(setup_db_with_group):
    db = setup_db_with_group
    db.cursor.execute("SELECT count(*) FROM subs_stat;")
    assert db.cursor.fetchone()[0] == 0
    db.db_insert_subs(1, 10)
    db.cursor.execute("SELECT group_id, subs_count FROM subs_stat;")
    assert db.cursor.fetchone() == (1, 10)
