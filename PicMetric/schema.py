from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class HashTable(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    original = DB.Column(DB.String(200), nullable=False)
    yolov3_source = DB.Column(DB.String(200), nullable=False)
    faces_source = DB.Column(DB.String(200), nullable=False)
    hash = DB.Column(DB.String(50), nullable=False)
    resnet = DB.Column(DB.String(500))
    yolov3 = DB.Column(DB.String(500))
