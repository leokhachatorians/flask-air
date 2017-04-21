import sqlalchemy
import sqlalchemy.types as sa_Types
import models
from initdb import session, metadata
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from wrappers import attempt_db_modification
from migrate.changeset import *

def generate_table(form, engine):
    """Generates a table

    Given a form object, get the name of the to be created table,
    insert and commit it into our Sheets table. Afterwords, refresh
    the metadata and use that to create a new table object which we
    then just simply create.
    """
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
    engine.connect().execute(ins)

def user_adds_column(form, sheet, schema):
    """Adds a user-defined column

    Gets the values from the form and creates a new row in
    Sheets, which is then added via the current session of new_col.
    It has to be the session pertaining to 'new_col' for some reason,
    otherwise it doesn't work. I forgot why :(

    After that, we need to create a reference to the generated table,
    create a column, and then create it via sqlalchemy-migrate.
    """
    schema_objects = schema.all()
    sequence_number = 0
    if len(schema_objects) > 0:
        sequence_number = schema_objects[-1].sequence_number + 1

    new_col = models.Sheets_Schema(
            sheet, form.column_name.data,
            form.types.data, sequence_number)

    current_session = session.object_session(new_col)
    current_session.add(new_col)
    current_session.commit()

    table = sqlalchemy.Table("table_{}".format(sheet.id), metadata)
    col = sqlalchemy.Column('col_{}'.format(new_col.id),
            getattr(sa_Types, new_col.column_type))
    col.create(table, populate_default=True)

def user_removes_columns(sheet, schema, request):
    """Deletes user defined columns

    Gather the columns the user wants to delete via the request and
    create a table which will "house" those columns.

    We can then delete the entry in sheets_schema and then have
    sqlalchemy-migrate drop the column via our "housing" table.

    Afterwards, we iterate over all the columns and adjust the sequence numbers
    before we actually delete the column in our schema table.
    """
    col_to_delete_id = request.form.getlist("to_delete")[0]
    col_to_delete = session.query(models.Sheets_Schema).filter_by(id=col_to_delete_id).one()

    # drop the given column from the given table
    sqlalchemy.Column("col_{}".format(col_to_delete_id)).drop(
            sqlalchemy.Table("table_{}".format(sheet.id), metadata))

    for col in session.query(models.Sheets_Schema).filter_by(sheet_id=sheet.id).all():
        if col.sequence_number > col_to_delete.sequence_number:
            col.sequence_number -= 1

    col_to_delete = session.query(models.Sheets_Schema).filter_by(id=col_to_delete_id).delete()
    session.commit()

def user_alters_column(edit_form, sheet, request):
    """Alters user picked columns

    Currently just queries the database and alters the name
    of the column. More work will be needed to properly adjust
    column types (ensure data correction, leave as-is, delete, etc)
    """
    col_to_alter_id = request.form.getlist("col_to_alter")[0]
    col = session.query(models.Sheets_Schema).filter_by(id=col_to_alter_id).one()
    col.column_name = edit_form.column_name.data
    col.column_type = edit_form.types.data
    session.commit()

def user_deletes_row(generated_table, row_id, engine):
    ins = generated_table.delete().where(generated_table.c.id==row_id)
    engine.connect().execute(ins)

def user_deletes_table(sheets, request):
    """Deletes a user generated tabled

    Based on the id of the sheet, remove the corresponding generated table,
    and the entry in 'Sheets' as well. Deletes the column definitions automatically.
    """
    sheet_to_drop_id = request.form.getlist("sheet_to_drop")[0]
    generate_table = sqlalchemy.Table("table_{}".format(sheet_to_drop_id), metadata).drop()
    session.query(models.Sheets).filter_by(id=sheet_to_drop_id).delete()
    session.commit()

def format_user_data(data):
    """
    Given various length tuples, trim the id and leave the rest
    intact to display to the user.
    """
    content = []
    for chunk in data:
        rows = []
        for i in chunk[1:]:
            rows.append(i)
        content.append(rows)
    return content
