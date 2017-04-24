import sqlalchemy
import sqlalchemy.types as sa_Types

class DTDataEngine():
    """Empty Abstract Base
    """
    pass

class DTDataEngineJSON(DTDataEngine):
    pass

class DTDataEngineSQL(DTDataEngine):
    def __init__(self, session, engine, metadata):
        self.session = session
        self.engine = engine
        self.metadata = metadata

    def set_schema(self, dtable, action):
        if action == 'add':
            self._add_column(dtable)
        elif action == 'alter':
            self._alter_column(dtable)
        elif action == 'remove':
            self._remove_column(dtable)
        elif action == 'generate':
            self._generate_table(dtable)
        elif action == 'drop':
            self._drop_table(dtable)

    def _add_column(self, dtable):
        table = sqlalchemy.Table("table_{}".format(dtable.id_), self.metadata)
        col = sqlalchemy.Column('col_{}'.format(dtable.info['modifications']['id']),
                getattr(sa_Types, dtable.info['modifications']['type']))
        col.create(table, populate_default=True)

    def _alter_column(self, dtable):
        pass

    def _remove_column(self, dtable):
        sqlalchemy.Column("col_{}".format(dtable.info['modifications']['id'])).drop(
                sqlalchemy.Table("table_{}".format(dtable.id_), self.metadata))

    def _generate_table(self, dtable):
        metadata = sqlalchemy.MetaData(self.engine)
        table = sqlalchemy.Table(
                'table_{}'.format(dtable.info['table_id']),
                metadata, sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True))
        metadata.create_all()

    def _drop_table(self, dtable):
        sqlalchemy.Table("table_{}".format(dtable.id_), self.metadata).drop()
        pass
