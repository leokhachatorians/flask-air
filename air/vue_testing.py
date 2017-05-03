import os
from flask import (
        Flask, request, session, g, redirect, url_for, abort,
        render_template, flash, current_app, jsonify
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

import forms, models, helpers

schema_store = DTSchemaStoreSQL(session, engine)
data_engine = DTDataEngineSQL(session, engine, metadata)

@app.route('/get_sheet')
def get_sheet_data():
    sheet = session.query(models.Sheets).filter_by(sheet_name="Applesauce").first()
    schema = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id).all()
    dtable = schema_store.get_schema(sheet.sheet_name, sheet.id)
    handle = data_engine.create_handle(dtable)
    contents = handle.get_rows(dtable)
    contents = helpers.format_user_data(schema, contents)
    return jsonify(contents)

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    sheet = session.query(models.Sheets).filter_by(id=data['sheet_id']).first()
    dtable = schema_store.get_schema(sheet.sheet_name, sheet.id)
    handle = data_engine.create_handle(dtable)

    schema = session.query(models.Sheets_Schema) \
            .filter(models.Sheets_Schema.sheet_id==sheet.id).all()
    data = {'col_{}'.format(schema[i].id): data['values'][i] for i, _ in enumerate(data)}
    handle.add_row(dtable, data)

    contents = handle.get_rows(dtable)
    contents = helpers.format_user_data(schema, contents)
    return jsonify(contents)

@app.route('/delete_data', methods=['POST'])
def delete_data():
    data = request.json
    dtable = schema_store.get_schema('_', data['sheet_id'])
    handle = data_engine.create_handle(dtable)
    handle.delete_row(dtable, data['row_id'])

    schema = session.query(models.Sheets_Schema) \
            .filter(models.Sheets_Schema.sheet_id==data['sheet_id']).all()

    contents = handle.get_rows(dtable)
    contents = helpers.format_user_data(schema, contents)
    return jsonify(contents)

@app.route('/modify_data', methods=['POST'])
def modify_data():
    data = request.json
    dtable = schema_store.get_schema('_', data['sheet_id'])
    handle = data_engine.create_handle(dtable)
    handle.update_row(dtable, data['row_id'], data['values'])

    schema = session.query(models.Sheets_Schema) \
        .filter(models.Sheets_Schema.sheet_id==data['sheet_id']).all()

    contents = handle.get_rows(dtable)
    contents = helpers.format_user_data(schema, contents)
    return jsonify(contents)

@app.route('/view_sheet/<sheet_name>')
def view_sheet(sheet_name):
    sheet = session.query(models.Sheets).filter_by(sheet_name=sheet_name).first()
    schema = session.query(models.Sheets_Schema).filter(models.Sheets_Schema.sheet_id==sheet.id).all()

    add_form = forms.AddDataForm(request.form)
    delete_form = forms.DeleteDataForm(request.form)
    edit_form = forms.EditDataForm(request.form)

    return render_template(
            'view_sheet_vue.html', sheet=sheet, add_form=add_form,
            delete_form=delete_form, edit_form=edit_form, schema=schema)

@app.route('/get_sheets')
def get_sheets():
    sheets = session.query(models.Sheets).filter_by(user_id=1).all()
    contents = {}
    contents['names'] = [sheet.sheet_name for sheet in sheets]
    return jsonify(contents)

@app.route('/')
def index():
    sheets = session.query(models.Sheets).filter_by(user_id=1).all()
    new_sheet_form = forms.NewSheetForm(request.form)
    delete_form = forms.DeleteTableForm(request.form)
    return render_template("index_vue.html", sheets=sheets,
            new_sheet_form=new_sheet_form, delete_form=delete_form)


if __name__ == "__main__":
    app.run(debug=True)
