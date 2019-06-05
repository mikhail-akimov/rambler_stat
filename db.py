import sqlite3


class DataBase:

    def __init__(self, db_address):
        self.conn = sqlite3.connect(db_address)
        self.cursor = self.conn.cursor()

    def db_init(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS
                            social_group(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name text UNIQUE
                                        )'''
                       )
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS
                            subs_stat(
                                    group_id INTEGER,
                                    stat_date datetime default CURRENT_TIMESTAMP,
                                    subs_count INTEGER,
                                    FOREIGN KEY(group_id) REFERENCES social_group(id)
                                    )'''
                       )
        self.conn.commit()

    def db_insert_group(self, group_name):
        sql = 'INSERT INTO social_group(name) VALUES(?)'
        self.cursor.execute(sql, [group_name])
        self.conn.commit()
        return True

    def db_check_group(self, group_name):
        sql = 'SELECT id FROM social_group where name=?'
        self.cursor.execute(sql, [group_name])
        result = self.cursor.fetchone()
        try:
            result = int(result[0])
        except:
            pass
        return result

    def db_insert_subs(self, group_id, subs_count):
        sql = 'INSERT INTO subs_stat (group_id, subs_count) VALUES(?, ?)'
        self.cursor.execute(sql, [group_id, subs_count])
        self.conn.commit()
        return True
