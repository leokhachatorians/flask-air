import sqlalchemy
import sqlalchemy.types as sa_Types
import models
from air import session
from wrappers import attempt_db_modification

def generate_table(data, db):
    metadata = sqlalchemy.MetaData(db.get_engine())
    names = [i for i in range(len(data['column_names']))]
    types = data['column_types']

    table = sqlalchemy.Table(
            'table_{}'.format(data['s_ID']), metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
            *(sqlalchemy.Column('col_{}'.format(name),
                getattr(sa_Types, _type)()) for (name, _type) in zip(names,types)))
    table.create()

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
    session.add(new_col)
