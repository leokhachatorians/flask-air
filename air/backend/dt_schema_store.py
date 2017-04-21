import models
import sqlalchemy
import sqlalchemy.types as sa_Types
from .dt_column import DTColumn
from .dtable import DTable

class DTSchema():
    """Empty Abstract Base
    """
    pass

class DTSchemaStoreJSON(DTSchema):
    pass

class DTSchemaStoreSQL(DTSchema):
    def __init__(self, session, engine, metadata):
        self.session = session
        self.engine = engine
        self.metadata = metadata

    def get_tables(self):
        pass

    def get_schema(self, table_id, table_name):
        dt_columns = []
        schema = self.session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==table_id).all()
        schema.sort(key=lambda x: x.sequence_number)
        for col in schema:
            dt_columns.append(DTColumn(col.id, col.column_name, col.column_type))
        return DTable(table_id, table_name, dt_columns)

    def set_schema(self, dtable, schema, sheet, action):
        if action == 'add':
            self._add_column(dtable, schema, sheet)
        elif action == 'alter':
            self._alter_column(dtable, sheet)
        elif action == 'remove':
            self._remove_column(dtable, schema, sheet)

    def _add_column(self, dtable, schema, sheet):
        schema_objects = schema.all()
        sequence_number = 0
        if len(schema_objects) > 0:
            sequence_number = schema_objects[-1].sequence_number + 1

        new_col = models.Sheets_Schema(
                sheet, dtable.info['modifications']['new']['name'],
                dtable.info['modifications']['new']['type'],
                sequence_number)

        current_session = self.session.object_session(new_col)
        current_session.add(new_col)
        current_session.commit()

        table = sqlalchemy.Table("table_{}".format(sheet.id), self.metadata)
        col = sqlalchemy.Column('col_{}'.format(new_col.id),
                getattr(sa_Types, new_col.column_type))
        col.create(table, populate_default=True)

    def _remove_column(self, dtable, schema, sheet):
        col_to_delete_id = dtable.info['modifications']['deleted']['id']
        col_to_delete = self.session.query(models.Sheets_Schema).filter_by(id=col_to_delete_id).one()

        # drop the given column from the given table
        sqlalchemy.Column("col_{}".format(col_to_delete_id)).drop(
                sqlalchemy.Table("table_{}".format(sheet.id), self.metadata))

        for col in self.session.query(models.Sheets_Schema).filter_by(sheet_id=sheet.id).all():
            if col.sequence_number > col_to_delete.sequence_number:
                col.sequence_number -= 1

        col_to_delete = self.session.query(models.Sheets_Schema).filter_by(id=col_to_delete_id).delete()
        self.session.commit()

    def _alter_column(self, dtable, sheet):
        pass
