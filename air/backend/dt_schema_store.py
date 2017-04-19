class DTSchemaStoreJSON():
    pass

class DTSchemaStoreSQL():
    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    def get_tables(self):
        pass

    def get_schema(self, table_name):
        pass

    def set_schema(self, table_name, table):
        pass
