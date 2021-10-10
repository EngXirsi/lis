# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/lis'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
#
# class lab_test(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     lab_test_name = db.Column(db.String(255))
#     mechine_name = db.Column(db.String(255))
#     mechine_modal = db.Column(db.String(255))
#     test_date = db.Column(db.String(255))
#     sent = db.Column(db.String(255))
#
# class test_result(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     lab_test_name = db.Column(db.String(255))
#     test_name = db.Column(db.String(255))
#     result = db.Column(db.String(255))
