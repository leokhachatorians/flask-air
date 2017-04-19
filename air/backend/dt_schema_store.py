import models
from .dt_column import DTColumn
from .dtable import DTable

class DTSchema():
    """Empty Abstract Base
    """
    pass

class DTSchemaStoreJSON(DTSchema):
    pass

class DTSchemaStoreSQL(DTSchema):
    def __init__(self, session, engine=None, metadata=None):
        self.session = session

    def get_tables(self):
        pass

    def get_schema(self, table_id, table_name):
        dt_columns = []
        schema = self.session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==table_id).all()
        schema.sort(key=lambda x: x.sequence_number)
        for col in schema:
            dt_columns.append(DTColumn(col.id, col.column_name, col.column_type))
        return DTable(table_id, table_name, dt_columns)


    def set_schema(self, table_name, table):
        pass
