import pytest
from db import DataBase


@pytest.fixture()
def setup():
    db = DataBase(':memory:')
    return db


def test_ab(setup):
    db = setup
    db.db_init()
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='social_group';")
    result = db.cursor.fetchone()
    assert 'social_group' in result
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='subs_stat';")
    result = db.cursor.fetchone()
    assert 'subs_stat' in result


# протестировать функцию get_subs (даём ей фиктивный ID группы, даём ей правдивый ID группы)

# проветирвоать db_insert_group (Селектим группу, которой нет, затем добавляем группу в БД и селектим её)

# проверить db_check_group (чекаем группу, которой нет, чекаем группу, которая есть)

# проверить db_insert_subs (проверяем, что записи по группе нет, добавляем запись и проверяем, что появились данные)
