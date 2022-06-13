import sqlite3
from sqlite3 import Error

class DBHelper:
    def __init__(self):
        self.connection = sqlite3.connect("game.sqlite", check_same_thread = False)
        self.cursor = self.connection.cursor()
        self.setup_db()

    def setup_db(self):
        argument = """
        CREATE TABLE IF NOT EXISTS game (
                id BIGINT NOT NULL PRIMARY KEY,
                name TEXT,
                score INT
        );
        """
        self.cursor.execute(argument)
        self.connection.commit()

    def add_user(self, values):
        argument = "INSERT INTO game ( id, name, score ) VALUES ( ?, ?, ? )"
        self.cursor.execute(argument, values)
        self.connection.commit()

    def update_score(self, values):
        argument = "UPDATE game SET score = ? WHERE id = ?"
        self.cursor.execute(argument, values)
        self.connection.commit()

    def get_score(self, id):
        argument = "SELECT score FROM game WHERE id = ?"
        self.cursor.execute(argument, ( id, ))

        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_leaderboard(self):
        argument = """
        SELECT id, name, score
            FROM game
            ORDER BY score
            DESC LIMIT 10
        """
        result = list()
        try:
            self.cursor.execute(argument)
            chunk_res = self.cursor.fetchall()
            for res in chunk_res:
                result.append({ "id": res[0], "name": res[1], "score": res[2] })
        except Error as e:
            pass

        return result

database = DBHelper()
