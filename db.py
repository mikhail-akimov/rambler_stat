import sqlite3

conn = sqlite3.connect("social_stat.db")
cursor = conn.cursor()


def db_init():
    cursor.execute('''CREATE TABLE IF NOT EXISTS
                        social_group(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name text UNIQUE
                                    )'''
                   )
    cursor.execute('''CREATE TABLE IF NOT EXISTS
                        subs_stat(
                                group_id INTEGER,
                                stat_date datetime default CURRENT_TIMESTAMP,
                                subs_count INTEGER,
                                FOREIGN KEY(group_id) REFERENCES social_group(id)
                                )'''
                   )
    conn.commit()


def db_insert_group(group_name):
    sql = 'INSERT INTO social_group(name) VALUES(?)'
    cursor.execute(sql, [group_name])
    conn.commit()
    return True


def db_check_group(group_name):
    sql = 'SELECT id FROM social_group where name=?'
    cursor.execute(sql, [group_name])
    result = cursor.fetchone()
    try:
        result = int(result[0])
    except:
        pass
    return result


def db_insert_subs(group_id, subs_count):
    sql = 'INSERT INTO subs_stat (group_id, subs_count) VALUES(?, ?)'
    cursor.execute(sql, [group_id, subs_count])
    conn.commit()
    return True
