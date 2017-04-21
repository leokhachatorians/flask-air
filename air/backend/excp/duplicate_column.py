class DuplicateColumnException(BaseException):
    """For when the column name already exists in the table"""
    def __init__(self, table_id, column_id, column_name):
        self.table_id = table_id
        self.column_id = column_id
        self.column_name = column_name

    def __str__(self):
        return (
            "Table <{}> already has a column <{}> with id <{}>.".format(
                self.table_id, self.column_name, self.column_id)
        )
