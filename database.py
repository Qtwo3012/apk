import sqlite3


class Database:

    def __init__(self, db_name="database/pattern.db"):

        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.create_table()

    # ==========================
    # Create Table
    # ==========================

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL

        )
        """)

        self.conn.commit()

    # ==========================
    # Insert
    # ==========================

    def insert(self, number):

        self.cursor.execute(
            "INSERT INTO history(number) VALUES(?)",
            (number,)
        )

        self.conn.commit()

    # ==========================
    # Get All
    # ==========================

    def get_all(self):

        self.cursor.execute(
            "SELECT number FROM history"
        )

        return [row[0] for row in self.cursor.fetchall()]

    # ==========================
    # Clear
    # ==========================

    def clear(self):

        self.cursor.execute(
            "DELETE FROM history"
        )

        self.conn.commit()

    # ==========================
    # Import Dataset
    # ==========================

    def import_dataset(self, dataset):

        self.clear()

        for number in dataset:
            self.insert(number)

    # ==========================
    # Total
    # ==========================

    def total(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM history"
        )

        return self.cursor.fetchone()[0]

    # ==========================
    # Close
    # ==========================

    def close(self):

        self.conn.close()