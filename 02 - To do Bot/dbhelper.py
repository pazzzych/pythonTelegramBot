import sqlite3

class DBHelper:
    # takes a database name 
    # (by default store our data in a file called todo.sqlite) 
    # and creates a database connection
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # creates a new table called items in our database 
    # This table has one column (called description)
    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (description text)"
        self.conn.execute(stmt)
        self.conn.commit()

    # takes the text for the item and inserts it into our database table
    def add_item(self, item_text):
        stmt = "INSERT INTO items (description) VALUES (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()
    
    # takes the text for an item and removes it from the database
    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    # returns a list of all the items in our database
    def get_items(self):
        stmt = "SELECT description FROM items"
        return [x[0] for x in self.conn.execute(stmt)]

