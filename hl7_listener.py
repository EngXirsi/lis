# Using the third party `aiorun` instead of the `asyncio.run()` to avoid
# boilerplate.
import aiorun
import asyncio
#import local_config as config
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import requests
from datetime import datetime
import json
import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
#import pickledb
from hl7 import parser

# import local_config as config
import hl7
from hl7.mllp import start_hl7_server
from hl7apy.parser import parse_message, parse_field
from hl7apy.core import Group, Segment
# from model import  lab_test , test_result ,db
from datetime import  datetime
# from local_config import  conn

# def insert_lab_test(lab_test_name , mechine_modal , mechine_name  ):
#     record = lab_test()
#     record.lab_test_name = lab_test_name
#     record.mechine_name = mechine_name
#     record.mechine_modal = mechine_modal
#     record.test_date = datetime.today()
#     record.sent = "No"
#     db.session.add(record)
#     db.session.commit()
# def insert_test_result(lab_test_name , test_name , result  ):
#     record = test_result()
#     record.lab_test_name = lab_test_name
#     record.test_name = test_name
#     record.result = result
#
#     db.session.add(record)
#     db.session.commit()


async def process_hl7_messages(hl7_reader, hl7_writer):
    """This will be called every time a socket connects
    with us.
    """
    # print("this is ", hl7_reader)
    peername = hl7_writer.get_extra_info("peername")
    print(f"Connection established {peername}")
    try:

        # We're going to keep listening until the writer
        # is closed. Only writers have closed status.
        while not hl7_writer.is_closing():

            hl7_message = await hl7_reader.readmessage()

            str_hl7_message = str(hl7_message)
            msg_lines = str_hl7_message.splitlines()
            msg =  hl7.parse(str_hl7_message)
            obxs = msg.segments("OBX")
            # print(obxs)
            for obx in obxs:
                result = str(obx).split("|")
                print(result[2])
            # msg.separator
            # lab_test_name = msg_lines[3].split('|')[3]
            # machine_model= msg_lines[0].split('|')[2]
            # machine_make= msg_lines[0].split('|')[3]
            #
            # # insert_lab_test(lab_test_name , machine_model , machine_make)
            obxs =  msg_lines[8:35]
            # msg = hl7.parse(hl7_message)
            # print(len(msg))
            # pid = msg.segments
            # print(pid)
            for i, obx in enumerate(obxs):
                ch1 = obx.find('^')
                ch2 = obx.find('^', ch1 + 1)
                test_name = obx[ch1 + 1:ch2]

                n1 = obx.find('|', ch2) + 1
                n2 = obx.find('|', n1 + 1)

                result = obx[n1 + 1:n2]
                # print(result)
               # insert_test_result(lab_test_name, test_name, result)
               #  try:
               #      pass
               #      # labdoc = conn.get_doc("Lab Test", lab_test_name)
               #      #print(labdoc)
               #      # if labdoc:
               #      #
               #      #     labdoc['normal_test_items'][i]['result_value'] = result
               #      #     conn.update(labdoc)
               #      #     print("Inserted")
               #  except:
               #      pass




            # hl7_writer.writemessage(hl7_message.create_ack())

            await hl7_writer.drain()
    except asyncio.IncompleteReadError:
        # Oops, something went wrong, if the writer is not
        # closed or closing, close it. dcr
        if not hl7_writer.is_closing():
            hl7_writer.close()
            await hl7_writer.wait_closed()
    print(f"Connection closed {peername}")

async def main():
    try:
        # Start the server in a with clause to make sure we
        # close it
        async with await start_hl7_server(
            process_hl7_messages,'192.168.100.5', port=5660,limit = 1024 * 128,
        ) as hl7_server:

            # And now we server forever. Or until we are
            # cancelled...
            await hl7_server.serve_forever()
    except asyncio.CancelledError:
        # Cancelled errors are expected
        pass
    except Exception:
        print("Error occurred in main")

def _safe_get_error_str(res):
    try:
        error_json = json.loads(res._content)
        if 'exc' in error_json:  # this means traceback is available
            error_str = json.loads(error_json['exc'])[0]
        else:
            error_str = json.dumps(error_json)
    except:
        error_str = str(res.__dict__)
    return error_str


def setup_logger(name, log_file, level=logging.INFO, formatter=None):

    if not formatter:
        formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')

    handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=50)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger


aiorun.run(main(), stop_on_unhandled_errors=True)
