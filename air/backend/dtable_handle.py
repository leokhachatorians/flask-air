class DTableHandle():
    """Handler to a generated table"""
    def __init__(self, dtable, data_engine):
        self.dtable = dtable
        self.data_engine = data_engine

    def get_row(self, dtable, row_id):
        return self.data_engine.get_row(dtable, row_id)

    def get_rows(self, dtable):
        return self.data_engine.get_rows(dtable)

    def add_row(self, dtable, data):
        self.data_engine.add_row(dtable, data)

    def delete_row(self, dtable, row_id):
        self.data_engine.delete_row(dtable, row_id)

    def update_row(self, dtable, row_id, data):
        self.data_engine.update_row(dtable, row_id, data)
