from wtforms import Form, BooleanField, StringField, PasswordField, validators

class NewSheetForm(Form):
    sheet_name = StringField('Sheet Name', [validators.Length(min=3, max=25), validators.DataRequired()])
    column_names = StringField('Column Names', [validators.Length(min=3, max=50), validators.DataRequired()])
    column_types = StringField('Column Types', [validators.Length(min=3, max=50), validators.DataRequired()])

class AddColumnForm(Form):
    column_name = StringField('Column Name', [validators.Length(min=3, max=25), validators.DataRequired()])
    column_type = StringField('Column Type', [validators.Length(min=3, max=25), validators.DataRequired()])

