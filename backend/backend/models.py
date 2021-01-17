from flask import url_for

from backend import db

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Text, unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    format = db.Column(db.Text, nullable=False)

    def __init__(self, key, value, format):
       self.key = key
       self.value = value
       self.format = format

    def __str__(self):
       return "{} {} {}".format(self.key,self.value,self.format)

    def __repr__(self):
       return "{} {} {}".format(self.key,self.value,self.format)

class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Text, primary_key=True)
    date_created = db.Column(db.Integer, nullable=False)
    date_updated = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, id, date_created, date_updated, text):
        self.id = id
        self.date_created = date_created
        self.date_updated = date_updated
        self.text = text

    def __str__(self):
       return "{} {} {} {}".format(self.id, self.date_created, self.date_updated, self.text)

    def __repr__(self):
       return "{} {} {} {}".format(self.id, self.date_created, self.date_updated, self.text)

