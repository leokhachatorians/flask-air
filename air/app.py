import os
from flask import (
        Flask, request, session, g, redirect, url_for, abort,
        render_template, flash, current_app
)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Table, MetaData
from initdb import session, metadata, engine
import sqlalchemy
from backend.dtable import DTable
from backend.dt_column import DTColumn
from backend.dt_schema_store import DTSchemaStoreSQL
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

schema_store = DTSchemaStoreSQL(session, engine, metadata)


@app.route('/', methods=['GET', 'POST'])
def index():
    # hard coding user id for the time being
    sheets = session.query(models.Sheets).filter_by(user_id=1).all()
    new_sheet_form = forms.NewSheetForm(request.form)
    delete_form = forms.BaseDeleteForm(request.form)

    if request.method == 'POST':
        if new_sheet_form.submit_new_sheet.data and new_sheet_form.validate():
            helpers.generate_table(new_sheet_form, engine)
            return redirect(url_for('index'))
        elif delete_form.submit_delete.data and delete_form.validate():
            helpers.user_deletes_table(sheets, request)
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

    dtable = schema_store.get_schema(sheet.id, sheet.sheet_name)

    if request.method == 'POST':
        if add_form.submit_add_data.data and add_form.validate():
            helpers.user_adds_data(generated_table, schema, request, engine)
        elif delete_form.submit_delete_row.data and delete_form.validate():
            helpers.user_deletes_row(generated_table, request.form.getlist('row_id')[0], engine)
        return redirect(url_for('view_sheet', sheet_name=sheet_name))

    # Make sure to close the session after querying the generated table,
    # otherwise the session keeps a lock on table for some reason.
    contents = session.query(generated_table).all()
    session.close()

    return render_template('view_sheet.html',
            schema=dtable.columns, sheet_name=sheet_name,
            contents=contents, add_form=add_form,
            delete_form=delete_form)

@app.route('/modify_sheet/<sheet_name>', methods=['GET', 'POST'])
def modify_sheet(sheet_name):
    """Allows the user to modify the open "Sheet".

    Two seperate forms exist, one for adding columns and the other
    for deletion. As such, there exists two blocks which handle
    each respective action.
    """
    add_form = forms.AddColumnForm(request.form)
    delete_form = forms.BaseDeleteForm(request.form)
    edit_form = forms.EditColumnForm(request.form)

    sheet = session.query(models.Sheets).filter_by(sheet_name=sheet_name).first()
    schema = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id)

    dtable = schema_store.get_schema(sheet.id, sheet.sheet_name)

    if request.method == 'POST':
        if add_form.submit_add_column.data and add_form.validate():
            result = dtable._add_column(add_form.column_name.data, add_form.types.data)
            if result:
                schema_store.set_schema(dtable, schema, sheet)
            else:
                print('duplicate column name')
        elif delete_form.submit_delete.data and delete_form.validate():
            helpers.user_removes_columns(sheet, schema, request)
        elif edit_form.submit_edit_column.data and edit_form.validate():
            helpers.user_alters_column(edit_form, sheet, request)
        return redirect(url_for('modify_sheet', sheet_name=sheet_name))
    return render_template('modify_sheet.html',
            schema=dtable.columns, add_form=add_form,
            delete_form=delete_form, edit_form=edit_form,
            sheet_name=sheet_name)

if __name__ == "__main__":
    app.run(debug=True)
