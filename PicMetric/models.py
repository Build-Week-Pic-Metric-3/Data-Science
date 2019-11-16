from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class HashTable(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    hash = DB.Column(DB.String(20), nullable=False)
    pred = DB.Column(DB.String(100), nullable=False)
    url = DB.Column(DB.String(100), nullable=False)
