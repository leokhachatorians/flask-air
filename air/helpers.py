import sqlalchemy
import sqlalchemy.types as sa_Types
import models
from air import session
from sqlalchemy import and_
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

def structure_alter_table_data(action, obj, **kwargs):
    """
    Given a DB object, create and structure data
    which will then be used to generate the SQL
    commands for alter the user's table.
    """
    if action == 'add_col':
        data = {
            'table_name': "table_{}".format(obj.id),
             'new_col': {
                'name': "col_{}".format(obj.column_num),
                'type': obj.column_type
            }
        }
    elif action == 'remove_col':
        data = {
            'table_name': "table_{}".format(obj.sheet_id),
            'remove_col': "col_{}".format(obj.column_num)
        }

    elif action == 'rename_col':
        data = {
            'table_name': "table_{}".format(obj.sheet_id),
            'rename_col': {
                'old_name': "col_{}".format(obj.column_num),
                'new_name': "col_{}".format(kwargs['new_col_num'])
            }
        }


    return data

def generate_alter_table_sql(action, data):
    """
    data = {
        'table_name': sheet_name,
        'new_col': {
            'name': name,
            'type': type
        }
        'remove_col': name,
        'rename_col': {
            'old_name': old_name,
            'new_name': new_name,
        }
        'rename_table': {
            'table': table_object,
            'new_table_name': new_table_name
        }
    }
    """
    if action == 'add_col':
        command = "ALTER TABLE {} ADD COLUMN {} {};".format(
                data['table_name'],
                data['new_col']['name'],
                data['new_col']['type'])

    elif action == 'remove_col':
        command = "ALTER TABLE {} DROP COLUMN {};".format(
                data['table_name'],
                data['remove_col'])

    elif action == 'rename_col':
        command = "ALTER TABLE {} RENAME COLUMN {} TO {};".format(
                data['table_name'],
                data['rename_col']['old_name'],
                data['rename_col']['new_name'])

    elif action == 'rename_table':
        pass
    elif action == 'change_col_type':
        pass
    return command

def user_adds_column(form, sheet, schema):
    new_col = models.Sheets_Schema(
            sheet, form.column_name.data,
            form.column_type.data, schema[-1].column_num + 1)

    current_session = session.object_session(new_col)
    current_session.add(new_col)
    current_session.commit()
    #return new_col

def user_removes_columns(sheet, schema, request):
        cols_to_delete = request.form.getlist("to_delete")
        commands = []
        for name in cols_to_delete:
            col_to_delete = session.query(models.Sheets_Schema).filter(and_(
                models.Sheets_Schema.column_name==name,
                models.Sheets_Schema.sheet_id==sheet.id)).delete()
          #  data = structure_alter_table_data('remove_col', col_to_delete)
          #  commands.append(generate_alter_table_sql(
          #      "remove_col", data))
          #  session.delete(col_to_delete)

        leftover_columns = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id).all()
        for i, col in enumerate(leftover_columns):

            col.column_num = i
            #data = structure_alter_table_data(
            #    'rename_col', col, new_col_num=col.column_num - num_dropped)
            #commands.append(generate_alter_table_sql(
            #    "rename_col", data))
        session.commit()

    #    return commands
