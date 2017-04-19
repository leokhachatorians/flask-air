class DTColumn():
    def __init__(self, column_id, column_name, column_type):
        self.column_id = column_id
        self.column_name = column_name
        self.column_type = column_type

    def _edit_name(self, new_name):
        self.column_name = new_name

    def _edit_type(self, new_type):
        self.column_type = new_type

    def __str__(self):
        return "<Name: {}>, <Type: {}>, <ID: {}>".format(
                self.column_name, self.column_type, self.column_id)
