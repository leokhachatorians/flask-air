class DTColumn():
    """Representation of a column

    DTColumn is essentially a holder of a users column. It doesn't hold any data
    other than the name of the column, the id (if it has one), and its type. It's
    used to help determine what actions should be taken by 'DT Schema Store' when
    updating a users table.
    """
    def __init__(self, column_id, column_name, column_type):
        self.column_id = column_id
        self.column_name = column_name
        self.column_type = column_type

    def edit_name(self, new_name):
        self.column_name = new_name

    def edit_type(self, new_type):
        self.column_type = new_type

    def __repr__(self):
        return "Name: {}, Type: {}, ID: {}".format(
                self.column_name, self.column_type, self.column_id)

    def __str__(self):
        return "Name: {}, Type: {}, ID: {}".format(
                self.column_name, self.column_type, self.column_id)
