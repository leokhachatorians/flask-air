from wtforms import (
        Form, BooleanField, StringField, PasswordField, validators,
        SubmitField,
)
from wtforms.widgets import CheckboxInput

import wtforms


class NewSheetForm(Form):
    sheet_name = StringField('Sheet Name',
            [validators.Length(min=3, max=25), validators.DataRequired()],
            render_kw={"placeholder": "People"})
    column_names = StringField('Column Names',
            [validators.Length(min=3, max=50), validators.DataRequired()],
            render_kw={"placeholder": "Name, Age, Location"})
    column_types = StringField('Column Types',
            [validators.Length(min=3, max=50), validators.DataRequired()],
            render_kw={"placeholder": "Text, Text, Text"})

class AddColumnForm(Form):
    column_name = StringField('Column Name',
            [validators.Length(min=3, max=25), validators.DataRequired()],
            render_kw={"placeholder": "PhoneNumber"})
    column_type = StringField('Column Type',
            [validators.Length(min=3, max=25), validators.DataRequired()],
            render_kw={"placeholder": "Text"})
    submit_add_column = SubmitField('Add Column')

class DeleteColumnForm(Form):
    submit_delete_columns = SubmitField('Delete Columns',
            render_kw={
                "class":"btn btn-xs btn-danger",
                "value": "Delete"
                }
    )
