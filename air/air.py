import os
import forms, helpers
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash, current_app
from flask_sqlalchemy import SQLAlchemy

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

import models

@app.route('/')
def index():
    return "Hello word"

@app.route('/create_new_sheet', methods=['GET', 'POST'])
def create_new_sheet():
    form = forms.NewSheetForm(request.form)
    if request.method == 'POST' and form.validate():
        sheet = models.Sheets(1, form.sheet_name.data)
        db.session.add(sheet)
        db.session.commit()

        data = helpers.standardize_form_data(form)
        data['s_ID'] = sheet.id

        for i, (c_name, c_type) in enumerate(zip(data['column_names'], data['column_types'])):
            schema = models.Sheets_Schema(sheet, c_name, c_type, i)
            db.session.add(schema)

        db.session.commit()
        helpers.generate_table(data)
        return redirect(url_for('create_new_sheet'))
    return render_template('create_new_sheet.html', form=form)

@app.route('/view_sheet/<sheet_name>')
def view_sheet(sheet_name):
    sheet = models.Sheets.query.filter_by(sheet_name=sheet_name).first()
    schema = models.Sheets_Schema.query.filter_by(sheet_id=sheet.id).all()
    return render_template('view_sheet.html', schema=schema)

if __name__ == "__main__":
    app.run(debug=True)
