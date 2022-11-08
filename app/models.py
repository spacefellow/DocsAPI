from init import db


class Document(db.Model):
    __searchable__ = ['text']
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=False, nullable=True)
    rubrics = db.Column(db.Text, unique=False, nullable=True)
    created_date = db.Column(db.String(255), unique=False, nullable=True)
