#!/bin/python3

from flask import Flask, request, json
from datetime import datetime
from dbconnection import DB_connection
import logging

app=Flask(__name__)
#   GET request always gets two variables key and value key=["date", "record_id"], value[ISODate, _id]
def processing_get(request):
    logging.info(request.args["value"])
    request_map ={ "key": request.args["key"], "value": request.args["value"]}
    record_id = db_connect.get_records(request_map, app.config["DATABASE"]["collection"])
    lines=""
    for el in record_id:
        lines+=f"{el}"
    return (lines)

#   POST request gets variable status: {"hostname": $hostname, "max_memory": $max_memory(int, megabytes), 
#       "used_memory": $used_memory(int, megabytes), "limit": $limit(float) }
def processing_post(request):
    time_stamp=datetime.now()
    req=request.get_json()
    status = req["status"]
    data={  "date": time_stamp,
            "hostname": status["hostname"],
            "max_memory": status["max_memory"],
            "used_memory" : status["used_memory"],
            "limit" : status["limit"]
            }
    record_id = db_connect.add_one_record(data, app.config["DATABASE"]["collection"])
    logging.info(f"record_id: {record_id}")
    return (f"_id: {record_id}")


#   PUT request gets two variables - status: {"hostname": $hostname, "max_memory": $max_memory(int, megabytes), 
#       "used_memory": $used_memory(int, megabytes), "limit": $limit(float) } and "record_id": _id
def processing_put(request):
    time_stamp=datetime.now()
    req=request.get_json()
    status = req["status"]
    record_id = req["record_id"]
    data={  "date": time_stamp,
            "hostname": status["hostname"],
            "max_memory": status["max_memory"],
            "used_memory" : status["used_memory"],
            "limit" : status["limit"]
            }
    record_id = db_connect.update_one(record_id, data, app.config["DATABASE"]["collection"])
    logging.info(f"record_id: {record_id}")
    return (f"_id: {record_id}")


#def processing_delete():
#    retur("DELETE")

@app.route("/", methods=['GET', 'POST', 'PUT'])
def get_message():
    logging.info('Connection')
    if request.method == 'GET':
        return processing_get(request)
    if request.method == 'POST':
        return processing_post(request)
    if request.method == 'PUT':
        return processing_put(request)
    else:
        logging.warning(f"record_id: {request.data}")
        return ('400')


if __name__ == '__main__':
    # Load configuration file
    app.config.from_file("config.json", load=json.load)
    credentials=app.config.get("DATABASE")
    logging.basicConfig(level=logging.getLevelName(app.config.get("LOGGER_LEVEL")))
    # Pass credentials for connecting database
    db_connect = DB_connection(credentials)
    app.run(host=app.config.get("SERVER_LISTEN"), port=app.config.get("SERVER_PORT"))
