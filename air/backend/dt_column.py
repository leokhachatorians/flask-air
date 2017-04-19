class DTColumn():
    def __init__(self, id_, name, type_, sequence_number):
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.sequence_number = sequence_number

    def _edit_name(self, new_name):
        self.name = new_name

    def _edit_type(self, new_type):
        self.type_ = new_type

    def __str__(self):
        return "<Name: {}>, <Type: {}>, <Sequence: {}>, <ID: {}>".format(
                self.name, self.type_, self.sequence_number, self.id_)
