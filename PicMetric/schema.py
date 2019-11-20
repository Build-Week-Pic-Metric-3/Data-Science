from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class HashTable(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    source = DB.Column(DB.String(100), nullable=False)
    hash = DB.Column(DB.String(50), nullable=False)
    resnet = DB.Column(DB.String(100))
    yolov3 = DB.Column(DB.String(100))