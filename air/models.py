from air import db, app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return "<User {}>".format(self.username)

class Sheets(db.Model):
    __tablename__ = 'sheets'
    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer)
    sheet_name = db.Column(db.String(180), unique=True)

    def __init__(self, user_id, sheet_name):
        self.user_id = user_id
        self.sheet_name = sheet_name

    def __repr__(self):
        return "<User's:{} Sheet_Name:{}>".format(
                self.user_id,
                self.sheet_name)

class Sheets_Schema(db.Model):
    __name__ = 'sheets_schema'
    id = db.Column(db.Integer, primary_key=True)
    sheet_id = db.Column(db.Integer, db.ForeignKey("sheets.id"))
    sheet = db.relationship('Sheets',
            backref=db.backref('sheets_scehma', lazy='dynamic'))
    column_name = db.Column(db.String(150), unique=True)
    column_type = db.Column(db.String(80))
    column_num = db.Column(db.Integer)

    def __init__(self, sheet, column_name, column_type, column_num):
        self.sheet = sheet
        self.column_name = column_name
        self.column_type = column_type
        self.column_num = column_num

    def __repr__(self):
        return "<Sheets_Schema {} {} {} {}>".format(
                self.sheet, self.column_name, self.column_type,
                self.column_num)
