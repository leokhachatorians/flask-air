import sqlalchemy
import sqlalchemy.types as sa_Types

from .dtable_handle import DTableHandle

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

    def set_schema(self, dtable):
        if dtable.info['action'] == 'add':
            self.add_column(dtable)
        elif dtable.info['action'] == 'alter':
            self.alter_column(dtable)
        elif dtable.info['action'] == 'remove':
            self.remove_column(dtable)
        elif dtable.info['action'] == 'generate':
            self.generate_table(dtable)
        elif dtable.info['action'] == 'drop':
            self.drop_table(dtable)

    def add_column(self, dtable):
        table = sqlalchemy.Table("table_{}".format(dtable.id_), self.metadata)
        col = sqlalchemy.Column('col_{}'.format(dtable.info['modifications']['id']),
                getattr(sa_Types, dtable.info['modifications']['type']))
        col.create(table, populate_default=True)

    def alter_column(self, dtable):
        pass

    def remove_column(self, dtable):
        sqlalchemy.Column("col_{}".format(dtable.info['modifications']['id'])).drop(
                sqlalchemy.Table("table_{}".format(dtable.id_), self.metadata))

    def generate_table(self, dtable):
        metadata = sqlalchemy.MetaData(self.engine)
        table = sqlalchemy.Table(
                'table_{}'.format(dtable.info['table_id']),
                metadata, sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True))
        metadata.create_all()

    def drop_table(self, dtable):
        sqlalchemy.Table("table_{}".format(dtable.id_), self.metadata).drop()

    def create_handle(self, dtable):
        return DTableHandle(dtable, self)

    def get_table(self, dtable):
        meta = sqlalchemy.MetaData(bind=self.engine)
        return sqlalchemy.Table("table_{}".format(dtable.id_), meta, autoload=True)

    def get_row(self, dtable, row_id):
        return self.session.query(self.get_table(dtable)).filter_by(id=row_id).one()

    def get_rows(self, dtable):
        return self.session.query(self.get_table(dtable)).order_by('id')

    def add_row(self, dtable, data):
        ins = self.get_table(dtable).insert().values(data)
        self.engine.connect().execute(ins)

    def delete_row(self, dtable, row_id):
        table = self.get_table(dtable)
        ins = table.delete().where(table.c.id==row_id)
        self.engine.connect().execute(ins)

    def update_row(self, dtable, row_id, data):
        """Update a generated table row contents

        Inspects the columns of the generated table, parses them and creates
        a dictionary of {'column_name': 'data'} which we then use to update the
        aforementioned row. Note that when we pass in the values to update,
        we have synchronize_session set to false. Since the generated
        tables aren't actually mapped to a SQLAlchemy class, inserting via
        query just wont work.
        """
        generated_table = self.get_table(dtable)
        table_name = "table_{}".format(dtable.id_)
        row = self.session.query(generated_table).filter_by(id=row_id).first()
        inspector = sqlalchemy.inspect(self.engine)
        column_names = [column['name'] for column in inspector.get_columns(table_name) if column['name'] != 'id']
        values = {col_name: data[i] for i, col_name in enumerate(column_names)}
        self.session.query(generated_table).filter_by(id=row_id).update(values, synchronize_session=False)
        self.session.commit()
