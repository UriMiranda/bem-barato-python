from tools.database import database

class Model:
    
    _query_values = list()
    _select_list = tuple()
    _query = ""

    def __init__(self):
        """ Start creating models table if not exists
            :return self: Returns self model
        """
        self.create_table()
        return None
    
    def select(self, *args):
        """ Create arguments select list to query
            :param args: Fields names
            :return self: Returns self model
        """
        self._select_list = self._select_list + args
        return self

    def where(self, **kwargs):
        """ Create SQL WHERE filters
            :param kwargs: Fields names and value to filter resultset
            :return self: Returns self model
        """
        fields, values = database.kwardsTransform(kwargs)
        self._query_values.extend(values)
        if len(self._query) is 0 and len(fields) is 1:
            self._query += " WHERE " + fields[0] +" = ?"
        elif len(self._query) is 0:
            self._query += " WHERE " + " = ? AND ".join(fields)
        else:
            self._query += " = ? AND ".join(fields)
        return self

    def get(self):
        """ Run query and return lines
            :return self: Returns 
        """
        select_list = ", ".join(self._select_list)
        if len(self._select_list) == 0:
            select_list = '*'
        select = "SELECT {} FROM {} {}".format(select_list, self._table, self._query)
        print(select)
        with database.create_connection() as conn:
            rows = database.execute(conn, select, self._query_values, True)
        return rows

    def save(self):
        model_attributes = self.__dict__
        fields, values = database.queryTransform(model_attributes)
        placeholders = "?,"*len(fields)
        sql = """INSERT INTO {} ({}) VALUES ({})""".format(self._table, ",".join(fields),placeholders.strip(','))
        print(sql)
        with database.create_connection() as conn:
            database.execute(conn, sql, values)