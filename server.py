from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Thiết lập kết nối MySQL
db = mysql.connector.connect(
    host="localhost",
    port=3336,
    user="root",
    password="",
    database="aochongchay"
)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    building_id = data['building_id']
    floor_id = data['floor_id']
    room_id = data['room_id']
    temperature = data['temperature']
    heart_rate = data['heart_rate']
    gas_concentration = data['gas_concentration']
    user_status = data['user_status']
    uuid = data['uuid']

    cursor = db.cursor()
    cursor.execute("INSERT INTO fireproof_jacket (building_id, floor_id, room_id, temperature, heart_rate, gas_concentration, user_status, uuid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )", (building_id, floor_id, room_id, temperature, heart_rate, gas_concentration, user_status, uuid))
    db.commit()

    return jsonify({"status": "success"}), 201

@app.route('/data', methods=['GET'])
def get_data():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fireproof_jacket")
    result = cursor.fetchall()
    return jsonify(result), 200

@app.route('/trangchitiet', methods=['GET'])
def get_data1():
    building_id = request.args.get('building_id')
    if building_id is None:
        return jsonify({"error": "Missing building_id"}), 400

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM building WHERE id = %s", (building_id,))

    result = cursor.fetchall()
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
