import psycopg2
import os


class DBHelper:
    def __init__(self, dbname="todo_list", username="todo_list", password='todolist'):
        DATABASE_URL = os.environ['DATABASE_URL']
        self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cur = self.connection.cursor()

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text);"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description);"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner);"
        self.cur.execute(tblstmt)
        self.cur.execute(itemidx)
        self.cur.execute(ownidx)
        self.connection.commit()

    def add_item(self, item_text, owner):
        owner = str(owner)
        stmt = "INSERT INTO items (description, owner) VALUES (%s, %s);"
        args = (item_text, owner)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def delete_item(self, item_text, owner):
        owner = str(owner)
        stmt = "DELETE FROM items WHERE description = (%s) AND owner = (%s);"
        args = (item_text, owner)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (%s);"
        args = (str(owner), )
        self.cur.execute(stmt, args)
        items = self.cur.fetchall()
        return [x[0] for x in items]
