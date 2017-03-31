import os
import forms, helpers
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash, current_app
#from generated_table import GeneratedTable
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base
import sqlalchemy

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI="postgresql://leo:{}@localhost:5432/flask_air".format(os.environ['my_password']),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='blahlbahblah',
    USERNAME='admin',
    PASSWORD='admin'
))

app.config.from_envvar('AIR_SETTINGS', silent=True)

db = SQLAlchemy(app)
Session = sessionmaker(bind=db.get_engine())
session = scoped_session(Session)
#engine = db.get_engine

import models

@app.route('/')
def index():
    # hard coding user id for the time being
    sheets = models.Sheets.query.filter_by(user_id=1).all()
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
        helpers.generate_table(data, db)
        return redirect(url_for('create_new_sheet'))
    return render_template('create_new_sheet.html', form=form)

@app.route('/view_sheet/<sheet_name>')
def view_sheet(sheet_name):
    sheet = session.query(models.Sheets).filter_by(sheet_name=sheet_name).first()
    schema = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id)
    return render_template('view_sheet.html',
            schema=schema, sheet_name=sheet_name)

@app.route('/modify_sheet/<sheet_name>', methods=['GET', 'POST'])
def modify_sheet(sheet_name):
    """
    View which allows the user to modify the open "Sheet".

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
            new_col = models.Sheets_Schema(
                    sheet, add_form.column_name.data,
                    add_form.column_type.data, schema[-1].column_num + 1)
            session.add(new_col)
            session.commit()

            data = {
                'table_name': 'table_{}'.format(new_col.sheet_id),
                'new_col': {
                    'name': 'col_{}'.format(new_col.column_num),
                    'type': new_col.column_type
                }
            }
            command = helpers.alter_table_flow('add_col', data)


        elif delete_form.submit_delete_columns.data and delete_form.validate():
            helpers.user_removes_columns(sheet, schema, request)

        return redirect(url_for('view_sheet', sheet_name=sheet_name))
    return render_template('modify_sheet.html',
            schema=schema, add_form=add_form,
            delete_form=delete_form, sheet_name=sheet_name)

@app.route('/test/<table_name>')
def test(table_name):
    Base = automap_base()

    # reflect the tables
    Base.prepare(db.get_engine(), reflect=True)
    print(Base.classes)
    classes = Base.classes
    for c in classes:
        print(c)
    table = classes['{}'.format(table_name)]
    print(dir(table))
    print(dir(table.col_0))
    sheet = session.query(models.Sheets).filter_by(sheet_name="test").first()
    schema = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id)
    session.add(table(col_0=23))
    session.commit()


   # names = []
   # types = []
   # for i in schema:
   #     names.append(i.column_name)
   #     types.append(i.column_type)
   # data = zip(names, types)

   # for name, _type in zip(names, types):
   #     print(name, _type)

   # Base = automap_base()

   # class GeneratedTable(Base):
   #     __tablename__ = "{}".format(table_name)
   #     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
   #    # def __init__(self, data):
   #    #     self.data = data

   #    #     for name, _type in self.data:
   #    #         setattr(self, name, (getattr(sqlalchemy.types,_type)()))
   #             #setattr(self, __tablename__, "test")

   # Base.prepare()
   # t = GeneratedTable()
   # #print(t.name)
   # print(dir(t))


    return "testing"

if __name__ == "__main__":
    app.run(debug=True)
