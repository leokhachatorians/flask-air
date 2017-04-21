class ColumnException(Exception):
    """Base exception for column related exceptions"""

class DuplicateColumn(ColumnException):
    """For when the column name already exists in the table"""
    def __init__(self, table_id, column_id, column_name):
        self.table_id = table_id
        self.column_id = column_id
        self.column_name = column_name
        err_msg = "Table <{}> already has a column <{}> with id <{}>.".format(
                self.table_id, self.column_name, self.column_id)
        super(ColumnException, self).__init__(self, err_msg)

class ColumnDoesntExist(ColumnException):
    """Column to be modified doesn't exist"""
