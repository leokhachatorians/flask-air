from wtforms import (
        Form, BooleanField, StringField, PasswordField, validators,
        SubmitField,
)
from wtforms.widgets import CheckboxInput

import wtforms

class NewSheetForm(Form):
    sheet_name = StringField('Sheet Name',
            [validators.Length(min=3, max=25), validators.DataRequired()],
            render_kw={
                "placeholder": "People",
                "class": "form-control"})
    submit_new_sheet = SubmitField('Create',
            render_kw={
                'class': 'btn btn-s btn-primary',
                'style': 'margin-bottom: 0;'})

class AddColumnForm(Form):
    column_name = StringField('Column Name',
            [validators.Length(min=3, max=25), validators.DataRequired()],
            render_kw={
                "placeholder": "Name",
                "class": "form-control"})
   # column_type = StringField('Column Type',
   #         [validators.Length(min=3, max=25), validators.DataRequired()],
   #         render_kw={"placeholder": "Text"})
    submit_add_column = SubmitField('Add',
            render_kw={
                "class": "btn btn-s btn-primary",
                "style": "margin-bottom: 0;"})

class DeleteColumnForm(Form):
    submit_delete_columns = SubmitField('Delete Columns',
            render_kw={
                "class":"btn btn-xs btn-danger",
                "value": "Delete"
                })
