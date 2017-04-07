import os
from flask import (
        Flask, request, session, g, redirect, url_for, abort,
        render_template, flash, current_app
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Table, MetaData
from initdb import session, metadata, engine
import sqlalchemy

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

#db = SQLAlchemy(app)
#metadata = MetaData(bind=db.get_engine)
#Session = sessionmaker(bind=engine)
#session = Session()

import forms, helpers, models

@app.route('/')
def index():
    # hard coding user id for the time being
    #sheets = models.Sheets.query.filter_by(user_id=1).all()
    sheets = session.query(models.Sheets).filter_by(user_id=1).all()
    return render_template("index.html", sheets=sheets)

@app.route('/create_new_sheet', methods=['GET', 'POST'])
def create_new_sheet():
    """
    View to handle user creation of new "Sheets".

    Data is standardized prior to it being read for table
    generation.
    """
    form = forms.NewSheetForm(request.form)
    if request.method == 'POST' and form.validate():
        sheet = models.Sheets(1, form.sheet_name.data)
        session.add(sheet)
        session.commit()

        data = helpers.standardize_form_data(form)
        data['s_ID'] = sheet.id

        for i, (c_name, c_type) in enumerate(zip(data['column_names'], data['column_types'])):
            schema = models.Sheets_Schema(sheet, c_name, c_type, i)
            session.add(schema)

        session.commit()
        helpers.generate_table(data, engine)
        return redirect(url_for('index'))
    return render_template('create_new_sheet.html', form=form)

@app.route('/view_sheet/<sheet_name>', methods=['GET', 'POST'])
def view_sheet(sheet_name):
    """Displays a users sheet

    Relies on creating a generated_table object which contains
    the same name as the user's table we want to access. That generated
    table is then the vehicle we use to actually insert and retrieve
    data.
    """
    sheet = session.query(models.Sheets).filter_by(sheet_name=sheet_name).first()
    schema = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id)
    meta = MetaData(bind=engine)
    generated_table = Table("table_{}".format(
        sheet.id), meta, autoload=True)

    if request.method == 'POST':
        table_values = {}
        for c, i in enumerate(request.form.getlist("add_records")):
            table_values['col_{}'.format(c)] = i
        ins = generated_table.insert().values(table_values)
        conn = engine.connect()
        result = conn.execute(ins)
        return redirect(url_for('view_sheet', sheet_name=sheet_name))

    contents = session.query(generated_table).all()
    contents = helpers.format_user_data(contents)

    return render_template('view_sheet.html',
            schema=schema, sheet_name=sheet_name,
            contents=contents)

@app.route('/modify_sheet/<sheet_name>', methods=['GET', 'POST'])
def modify_sheet(sheet_name):
    """Allows the user to modify the open "Sheet".

    Two seperate forms exist, one for adding columns and the other
    for deletion. As such, there exists two blocks which handle
    each respective action.
    """
    add_form = forms.AddColumnForm(request.form)
    delete_form = forms.DeleteColumnForm(request.form)
    sheet = session.query(models.Sheets).filter_by(sheet_name=sheet_name).first()
    schema = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id)

    if request.method == 'POST':
        if add_form.submit_add_column.data and add_form.validate():
            helpers.user_adds_column(add_form, sheet, schema)
            #data = helpers.structure_alter_table_data('add_col', new_col)
            #command = helpers.generate_alter_table_sql('add_col', data)
        elif delete_form.submit_delete_columns.data and delete_form.validate():
            helpers.user_removes_columns(sheet, schema, request)

        return redirect(url_for('modify_sheet', sheet_name=sheet_name))
    return render_template('modify_sheet.html',
            schema=schema, add_form=add_form,
            delete_form=delete_form, sheet_name=sheet_name)

if __name__ == "__main__":
    app.run(debug=True)
