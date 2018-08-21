import sqlite3
from sqlite3 import Error

class database:
    @staticmethod
    def create_connection():
        """Create a connection with SQLite database
            :param self: database class
        """
        try:
            connection = sqlite3.connect('./resources/db/bem-barato.db')
            return connection
        except Error as e:
            print(e)
        return None
    
    @staticmethod
    def execute(conn, create_table_sql, values=None, fetchRows=False):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            if values is None:
                c.execute(create_table_sql)
            else:
                if fetchRows == True:
                    c.execute(create_table_sql, values)
                    rows = c.fetchall()
                    return rows
                else:
                    c.execute(create_table_sql, values)
        except Error as e:
            print(e)
    
    @staticmethod
    def queryTransform(query_values):
        fields = list()
        values = tuple()
        for key, value in query_values.items():
            fields.append(key)
            values = values + (value, )
        return fields, values

    @staticmethod
    def kwardsTransform(query_values):
        fields = list()
        values = tuple()
        for key, value in query_values.items():
            fields.append(key)
            values = values + (value, )
        return fields, values