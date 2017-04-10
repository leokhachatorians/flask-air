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
    if len(schema[:]) > 0:
        column_num = schema[-1].column_num + 1
    else:
        column_num = 0

    new_col = models.Sheets_Schema(
            sheet, form.column_name.data,
            form.column_type.data,
            column_num)

    current_session = session.object_session(new_col)
    current_session.add(new_col)
    current_session.commit()

    table = sqlalchemy.Table("table_{}".format(sheet.id),
            metadata)
    col = sqlalchemy.Column('col_{}'.format(new_col.column_num),
            getattr(sa_Types, new_col.column_type))
    col.create(table, populate_default=True)

def user_removes_columns(sheet, schema, request):
    """Deletes user defined columns

    Gather the columns the user wants to delete via the request and
    create a table which will "house" those columns.

    Afterwards iterate over the to-be-deleted coulmns, query Sheets_Schema
    to get the proper column_num, and then create a new column with simply
    the name of the column num. We can then delete the entry in sheets_schema
    and then have sqlalchemy-migrate drop the column via our "housing" table.
    """
    cols_to_delete = request.form.getlist("to_delete")
    generated_table = sqlalchemy.Table("table_{}".format(sheet.id),
            metadata)
    for name in cols_to_delete:
        col_to_delete = session.query(models.Sheets_Schema).filter(and_(
            models.Sheets_Schema.column_name==name,
            models.Sheets_Schema.sheet_id==sheet.id)).one()
        col = sqlalchemy.Column("col_{}".format(col_to_delete.column_num))
        session.delete(col_to_delete)
        session.commit()
        col.drop(generated_table)

        leftover_columns = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id).all()
        for i, col in enumerate(leftover_columns):
            #print(dir(generated_table))
            #test.alter(name='col_{}'.format(i))
            ##generated_table.c.
            ##left_col..alter(name="col_{}".format(i))
            ##left_col.column_num = i
            col.column_num = i
        session.commit()

def format_user_data(data):
    content = []
    for chunk in data:
        rows = []
        for i in chunk[1:]:
            rows.append(i)
        content.append(rows)
    return content
