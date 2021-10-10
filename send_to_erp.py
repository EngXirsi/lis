# import json
#
# import requests
# from celery import Celery
# from celery.schedules import crontab
# from local_config import conn
# from flask_sqlalchemy import SQLAlchemy
# from model import lab_test , test_result
# from datetime import datetime
# app = Celery()
# app.conf.broker_url = 'redis://localhost:6379/0'
# app.conf.result_backend = 'redis://localhost:6379/0'
# import local_config as config
#
# # labdoc = conn.get_doc("Lab Test")
# # users = conn.get_list('Patient')
#
# #
# # tests = test_result.query.filter_by(lab_test_name="30").all()
# # labdoc = conn.get_doc("Lab Test" , "LP-614642")
# # print(len(tests))
# # for i , test in enumerate(tests):
# #     labdoc['normal_test_items'][i]['result_value'] = ''
# # conn.update(labdoc)
# # print("ok")
#
#
#
# @app.task(name = 'send_data')
# def send_data():
#     try:
#         lab_tests = lab_test.query.filter_by(sent='No').all()
#
#         for lab in lab_tests:
#             labdoc = conn.get_doc("Lab Test" , lab.lab_test_name)
#             tests = test_result.query.filter_by(lab.lab_test_name).all()
#             for i, test in enumerate(tests):
#                 labdoc['normal_test_items'][i]['result_value'] = test.result
#             conn.update(labdoc)
#             lab.sent = "Yes"
#     except Exception as e:
#         print(e)
#
# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'send_data',
#         'schedule': 5.0,
#
#     },
# }
# app.conf.timezone = 'UTC'