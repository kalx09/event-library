import pymysql


class DatabaseConnection:
    """Represent a connection on a MySQL database."""

    def __init__(self,host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.create_connection()

    def create_connection(self):
        """Create a connection to the MySQL database using arguments."""
        try:
            cursor = pymysql.cursors.DictCursor
            self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database,
                                              port=self.port, cursorclass=cursor)
        except DatabaseException as exc:
            raise DatabaseException("Unable to make a connection to mysql database")

    def execute(self, request, *params):
        """Execute a sql statement against the database."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(request, *params)
            self.connection.commit()

            return ResultSet(cursor)
        except DatabaseException as exc:
            raise DatabaseException("Mysql query failed")


class DatabaseException(Exception):
    """The only exception class thrown by this module."""
    pass


class ResultSet():
    """Represent one or multiple rows following the execution of a request against the database.
    Access the result of the SQL query."""

    def __init__(self, cursor):
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._cursor)

    def get_rows(self):
        return self._cursor.fetchall()

    def row_count(self):
        """Return the number of row."""
        return self._cursor.rowcount

    def has_row(self):
        """Verify if the object has at least one row."""
        return self._cursor.rowcount > 0

    def status_message(self):
        """Return the status message on the cursor."""
        return self._cursor.statusmessage


db_obj = DatabaseConnection("127.0.0.1", 3306, "event", "root", "")