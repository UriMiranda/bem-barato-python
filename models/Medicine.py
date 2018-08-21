from models.Model import Model
from tools.database import database

class Medicine(Model):
    _table = 'medicines'

    def create_table(self):
        table = """CREATE TABLE IF NOT EXISTS {} (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name text NOT NULL,
                                    mcg text,
                                    drugstore text,
                                    price real NOT NULL,
                                    created_at text NOT NULL);""".format(self._table)
        with database.create_connection() as conn:
            database.execute(conn, table)
    

    def orWhere(self, **kwargs):
        fields, values = database.kwardsTransform(kwargs)
        
        return self
    

