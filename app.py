import os
from flask import Flask, Response, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
mongo_db_url = os.environ.get("MONGO_DB_CONN_STRING")

client = MongoClient(mongo_db_url)
db = client['sensors_db']

@app.get("/api/sensors")
def get_sensors():
    sensor_id = request.args.get('sensor_id')
    filter = {} if sensor_id is None else {"sensor_id": sensor_id}
    sensors = list(db.sensors.find(filter))

    response = Response(
        response=dumps(sensors), status=200,  mimetype="application/json")
    return response

@app.post("/api/sensors")
def add_sensor():
    _json = request.json
    db.sensors.insert_one(_json)

    resp = jsonify({"message": "Sensor added successfully"})
    resp.status_code = 200
    return resp


@app.delete("/api/sensors/<id>")
def delete_sensor(id):
    db.sensors.delete_one({'_id': ObjectId(id)})

    resp = jsonify({"message": "Sensor deleted successfully"})
    resp.status_code = 200
    return resp 

@app.put("/api/sensors/<id>")
def update_sensor(id):
    _json = request.json
    db.sensors.update_one({'_id': ObjectId(id)}, {"$set": _json})

    resp = jsonify({"message": "Sensor updated successfully"})
    resp.status_code = 200
    return resp