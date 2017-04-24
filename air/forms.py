from wtforms import (
        Form, BooleanField, StringField, PasswordField, validators,
        SubmitField, SelectField, FieldList, FormField,
)
from wtforms.widgets import CheckboxInput, SubmitInput

import wtforms

class Base():
    """Abstract Form which holds commonly used fields/values"""
    column_type_choices = [
                ('String', 'Text'), ('Text', 'Long Text'),
                ('Text', 'Select'), ('Boolean', 'Check Box'),
                ('Date', 'Date'), ('Text', 'Record'),
                ('Float', 'Currency'), ('Float', 'Number'),
                ('DateTime', 'Timestamp'), ('BigInteger', 'Integer'),
                ('String', 'Time')]

    hidden_field = StringField('',
            [validators.Length(min=1), validators.DataRequired()],
            render_kw={'type': 'hidden'})

class NewSheetForm(Form):
    sheet_name = StringField('Sheet Name',
            [validators.Length(min=1, max=25), validators.DataRequired()],
            render_kw={
                "placeholder": "People",
                "class": "form-control"})

    submit_new_sheet = SubmitField('Create',
            render_kw={
                'class': 'btn btn-s btn-primary',
                'style': 'margin-bottom: 0;'})

class AddColumnForm(Form):
    add_column_name = StringField('Column Name',
            [validators.Length(min=1, max=25), validators.DataRequired()],
            render_kw={
                "placeholder": "Name",
                "class": "form-control"})

    types = SelectField('Type',
            choices = Base.column_type_choices,
            render_kw={"class": "form-control",})

    submit_add_column = SubmitField('Add',
            render_kw={
                "class": "btn btn-s btn-primary",
                "style": "margin-bottom: 0;"})

class AddDataForm(Form):
    submit_add_data = SubmitField('Add',
            render_kw={
                "class": "btn btn-s btn-primary",
                "style": "margin-bottom: 0;"})

class DeleteDataForm(Form):
    delete_row_id = Base.hidden_field
    submit_delete_row = SubmitField('X',
            render_kw={
                'class': 'btn btn-xs btn-danger',
                'style': 'margin-bottom: 0;'})

class EditColumnForm(Form):
    edit_column_name = StringField('New Column Name',
            [validators.Length(min=1, max=25), validators.DataRequired()],
            render_kw={
                "placeholder": "Name",
                "class": "form-control"})

    types = SelectField('Type',
            choices=Base.column_type_choices,
            render_kw={"class": "form-control",})

    column_id = Base.hidden_field

    old_column_name = Base.hidden_field

    submit_edit_column = SubmitField('Save',
            render_kw={
                "class": "btn btn-s btn-success",
                "style": "margin-bottom: 0;"})

class DeleteColumnForm(Form):
    delete_column_name = Base.hidden_field

    delete_column_id = Base.hidden_field

    submit_delete = SubmitField('Delete',
            render_kw={
                "class":"btn btn-xs btn-danger",
                "style": "margin-bottom: 0",
                })

class DeleteTableForm(Form):
    submit_delete = SubmitField('Delete',
            render_kw={
                "class":"btn btn-xs btn-danger",
                "style": "margin-bottom: 0",
                })

    delete_table_id = Base.hidden_field

    delete_table_name = Base.hidden_field
