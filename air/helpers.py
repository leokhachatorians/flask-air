import sqlalchemy
import sqlalchemy.types as sa_Types
import models
from initdb import session, metadata
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from wrappers import attempt_db_modification
from migrate.changeset import *

def generate_table(data, engine):
    metadata = sqlalchemy.MetaData(engine)
    names = [i for i in range(len(data['column_names']))]
    types = data['column_types']

    table = sqlalchemy.Table(
            'table_{}'.format(data['s_ID']), metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
            *(sqlalchemy.Column('col_{}'.format(name),
                getattr(sa_Types, _type)()) for (name, _type) in zip(names,types)))
    metadata.create_all()

def generate_table_test(name, parent_sheet_id, engine):
    metadata = sqlalchemy.MetaData(engine)
    table = sqlalchemy.Table(
            'table_{}'.format(parent_sheet_id), metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True))
    metadata.create_all()

def standardize_form_data(form):
    """
    Given a form, attempt to standardize the
    data to be acceptable for Postgres
    """
    name = form.sheet_name.data
    column_names = form.column_names.data.split(',')
    column_types = form.column_types.data.split(',')

    for i, _name in enumerate(column_names):
        # Messy, but works. Names and types should
        # be equal in length.
        column_names[i] = _name.strip()
        column_types[i] = column_types[i].strip()

    for i, _type in enumerate(column_types):
        if _type == "Text":
            column_types[i] = "Text"
        elif _type == "Number":
            column_types[i] = "Text"
        elif _type == "Date":
            column_types[i] = "Date"
        elif _type == "File or Photo":
                column_types[i] = "LargeBinary"
        else:
            column_types[i] = "Text"

    data = {
            "table_name": name,
            "column_names": column_names,
            "column_types": column_types
    }

    return data

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
