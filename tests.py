import pytest
import sqlite3
from db import db_init


@pytest.fixture()
def setup():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    return conn, cursor


def test_ab(setup):
    conn, cursor = setup
    db_init()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='social_group';")
    result = cursor.fetchone()
    assert 'social_group' in result
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='subs_stat';")
    result = cursor.fetchone()
    assert 'subs_stat' in result


# протестировать функцию get_subs (даём ей фиктивный ID группы, даём ей правдивый ID группы)

# протестировать db_init (создаём базу в памяти, проверяем что структура соответствует требуемой)

# проветирвоать db_insert_group (Селектим группу, которой нет, затем добавляем группу в БД и селектим её)

# проверить db_check_group (чекаем группу, которой нет, чекаем группу, которая есть)

# проверить db_insert_subs (проверяем, что записи по группе нет, добавляем запись и проверяем, что появились данные)
