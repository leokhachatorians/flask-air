import sqlalchemy
import sqlalchemy.types as sa_Types
import models
from initdb import session, metadata
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from wrappers import attempt_db_modification
from migrate.changeset import *

def generate_table(form, engine):
    name = form.sheet_name.data
    sheet = models.Sheets(1, form.sheet_name.data)
    session.add(sheet)
    session.commit()

    metadata = sqlalchemy.MetaData(engine)
    table = sqlalchemy.Table(
            'table_{}'.format(sheet.id), metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True))
    metadata.create_all()

def user_adds_data(generated_table, schema, request, engine):
    table_values = {}
    for index, value in enumerate(request.form.getlist("add_records")):
        table_values['col_{}'.format(schema[index].id)] = value
    ins = generated_table.insert().values(table_values)
    conn = engine.connect()
    result = conn.execute(ins)

def user_adds_column(form, sheet, schema):
    """Adds a user-defined column

    Gets the values from the form and creates a new row in
    Sheets, which is then added via the current session of new_col.
    It has to be the session pertaining to 'new_col' for some reason,
    otherwise it doesn't work. I forgot why :(

    After that, we need to create a reference to the generated table,
    create a column, and then create it via sqlalchemy-migrate.
    """

    new_col = models.Sheets_Schema(
            sheet, form.column_name.data,
            'Text',) # hard coding type to 'Text' for the moment

    current_session = session.object_session(new_col)
    current_session.add(new_col)
    current_session.commit()

    table = sqlalchemy.Table("table_{}".format(sheet.id),
            metadata)
    col = sqlalchemy.Column('col_{}'.format(new_col.id),
            getattr(sa_Types, new_col.column_type))
    col.create(table, populate_default=True)

def user_removes_columns(sheet, schema, request):
    """Deletes user defined columns

    Gather the columns the user wants to delete via the request and
    create a table which will "house" those columns.

    We can then delete the entry in sheets_schema and then have
    sqlalchemy-migrate drop the column via our "housing" table.
    """
    col_to_delete_id = request.form.getlist("to_delete")[0]
    generated_table = sqlalchemy.Table("table_{}".format(sheet.id), metadata)
    generated_col_to_delete = sqlalchemy.Column("col_{}".format(col_to_delete_id))
    generated_col_to_delete.drop(generated_table)
    col_to_delete = session.query(models.Sheets_Schema).filter_by(id=col_to_delete_id).delete()
    session.commit()

def user_alters_column(edit_form, sheet, request):
    """
    def upgrade(migrate_engine):
        meta = MetaData(bind=migrate_engine)
        users = Table('users', meta, autoload=True)
        users.c.user_id.alter(name='id')

    from sqlalchemy import update

    stmt = update(users).where(users.c.id==5).\
            values(name='user #5')

    """
    col_to_alter_id = request.form.getlist("col_to_alter")[0]
    col = session.query(models.Sheets_Schema).filter_by(id=col_to_alter_id).one()
    col.column_name = edit_form.column_name.data
    session.commit()
    #table = sqlalchemy.Table("table_{}".format(sheet.id), metadata, autoload=True)

def user_deletes_table(sheets, request):
    sheet_to_drop_id = request.form.getlist("sheet_to_drop")[0]
    generate_table = sqlalchemy.Table("table_{}".format(sheet_to_drop_id), metadata).drop()
    session.query(models.Sheets).filter_by(id=sheet_to_drop_id).delete()
    session.commit()

def format_user_data(data):
    content = []
    for chunk in data:
        rows = []
        for i in chunk[1:]:
            rows.append(i)
        content.append(rows)
    return content
