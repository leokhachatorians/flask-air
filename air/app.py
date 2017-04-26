import os
from flask import (
        Flask, request, session, g, redirect, url_for, abort,
        render_template, flash, current_app
)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Table, MetaData
from initdb import session, metadata, engine
import sqlalchemy
from backend.dt_schema_store import DTSchemaStoreSQL
from backend.dt_data_engine import DTDataEngineSQL
from backend.excp.column_exceptions import DuplicateColumn

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI="postgresql://leo:password@localhost:5432/flask_air",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='blahlbahblah',
    USERNAME='admin',
    PASSWORD='admin'
))

app.config.from_envvar('AIR_SETTINGS', silent=True)

import forms, helpers, models

schema_store = DTSchemaStoreSQL(session, engine)
data_engine = DTDataEngineSQL(session, engine, metadata)

@app.route('/', methods=['GET', 'POST'])
def index():
    # hard coding user id for the time being
    sheets = session.query(models.Sheets).filter_by(user_id=1).all()
    new_sheet_form = forms.NewSheetForm(request.form)
    delete_form = forms.DeleteTableForm(request.form)

    if request.method == 'POST':
        if new_sheet_form.submit_new_sheet.data and new_sheet_form.validate():
            dtable = schema_store.get_schema(new_sheet_form.sheet_name.data)
            dtable.info['action'] = 'generate'
            schema_store.set_schema(dtable)
            data_engine.set_schema(dtable)
            return redirect(url_for('index'))
        elif delete_form.submit_delete.data and delete_form.validate():
            sheet_name = delete_form.delete_table_name.data
            sheet_id = delete_form.delete_table_id.data
            dtable = schema_store.get_schema(sheet_name, sheet_id)
            dtable.info['action'] = 'drop'
            schema_store.set_schema(dtable)
            data_engine.set_schema(dtable)
            return redirect(url_for('index'))
    return render_template("index.html", sheets=sheets,
            new_sheet_form=new_sheet_form, delete_form=delete_form)

@app.route('/view_sheet/<sheet_name>', methods=['GET', 'POST'])
def view_sheet(sheet_name):
    """Displays a users sheet

    Relies on creating a generated_table object which contains
    the same name as the user's table we want to access. That generated
    table is then the vehicle we use to actually insert and retrieve
    data.
    """
    sheet = session.query(models.Sheets).filter_by(sheet_name=sheet_name).first()
    schema = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id).all()
    meta = MetaData(bind=engine)

    generated_table = Table("table_{}".format(sheet.id), meta, autoload=True)

    add_form = forms.AddDataForm(request.form)
    delete_form = forms.DeleteDataForm(request.form)
    edit_form = forms.EditDataForm(request.form)

    dtable = schema_store.get_schema(sheet.sheet_name, sheet.id)
    handle = data_engine.create_handle(dtable)

    if request.method == 'POST':
        if add_form.submit_add_data.data and add_form.validate():
            data = request.form.getlist("add_records")
            data = {'col_{}'.format(schema[i].id): data[i] for i, _ in enumerate(data)}
            handle.add_row(dtable, data)
        elif delete_form.submit_delete_row.data and delete_form.validate():
            handle.delete_row(dtable, delete_form.delete_row_id.data)
        elif edit_form.submit_edit_row.data and edit_form.validate():
            handle.update_row(dtable, edit_form.edit_row_id.data, request.form.getlist('updated_cells'))
        return redirect(url_for('view_sheet', sheet_name=sheet_name))

    # Make sure to close the session after querying the generated table,
    # otherwise the session keeps a lock on table for some reason.
    contents = handle.get_rows(dtable)
    session.close()

    return render_template('view_sheet.html',
            schema=dtable.columns, sheet_name=sheet_name,
            contents=contents, add_form=add_form,
            delete_form=delete_form, edit_form=edit_form)

@app.route('/modify_sheet/<sheet_name>', methods=['GET', 'POST'])
def modify_sheet(sheet_name):
    """Allows the user to modify the open "Sheet".

    Two seperate forms exist, one for adding columns and the other
    for deletion. As such, there exists two blocks which handle
    each respective action.
    """
    sheet = session.query(models.Sheets).filter_by(sheet_name=sheet_name).first()
    schema = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id)

    add_form = forms.AddColumnForm(request.form)
    delete_form = forms.DeleteColumnForm(request.form)
    edit_form = forms.EditColumnForm(request.form)

    dtable = schema_store.get_schema(sheet.sheet_name, sheet.id)

    if request.method == 'POST':
        if add_form.submit_add_column.data and add_form.validate():
            if dtable.add_column(add_form):
                schema_store.set_schema(dtable, schema, sheet)
                data_engine.set_schema(dtable)
            else:
                print('duplicate column name')
        elif delete_form.submit_delete.data and delete_form.validate():
            if dtable.remove_column(delete_form):
                schema_store.set_schema(dtable, schema, sheet)
                data_engine.set_schema(dtable)
            else:
                print('invalid col id')
        elif edit_form.submit_edit_column.data and edit_form.validate():
            if dtable.alter_column(edit_form):
                schema_store.set_schema(dtable, schema, sheet)
                data_engine.set_schema(dtable)
            else:
                print('invalid')
        return redirect(url_for('modify_sheet', sheet_name=sheet_name))
    return render_template('modify_sheet.html',
            schema=dtable.columns, add_form=add_form,
            delete_form=delete_form, edit_form=edit_form,
            sheet_name=sheet_name)

if __name__ == "__main__":
    app.run(debug=True)
