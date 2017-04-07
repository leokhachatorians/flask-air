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
    new_col = models.Sheets_Schema(
            sheet, form.column_name.data,
            form.column_type.data, schema[-1].column_num + 1)

    current_session = session.object_session(new_col)
    current_session.add(new_col)
    current_session.commit()

    table = sqlalchemy.Table("table_{}".format(sheet.id),
            metadata)
    col = sqlalchemy.Column('col_{}'.format(new_col.column_num),
            getattr(sa_Types, new_col.column_type))
    table.append_column(col)
    col.create(table, populate_default=True)

def user_removes_columns(sheet, schema, request):
        cols_to_delete = request.form.getlist("to_delete")
        commands = []
        for name in cols_to_delete:
            col_to_delete = session.query(models.Sheets_Schema).filter(and_(
                models.Sheets_Schema.column_name==name,
                models.Sheets_Schema.sheet_id==sheet.id)).delete()

        leftover_columns = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id).all()
        for i, col in enumerate(leftover_columns):
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
