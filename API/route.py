from flask import Flask,jsonify,request
from datetime import datetime, UTC
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests

app = Flask(__name__)

# Konfigurasi MongoDB
MONGO_URI = "mongodb+srv://raflifirrizqiardi:Kepotapean@mancingcluster.qw1ff.mongodb.net/?retryWrites=true&w=majority&appName=mancingCluster"
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client['SensorDatabase']
collection = db['Assignment2']

# Snd a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
# Konfigurasi Ubidots
UBIDOTS_TOKEN = "BBUS-5PvX46FCIKJ7h2XyFIKhSgC7dcTCHA"
UBIDOTS_DEVICE_LABEL = "esp32-sic6"

def send_to_ubidots(temp, hum, pir, ultra, timestamp):
    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/"
    headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}
    payload = {"temp": temp, "humidity": hum, "pir": pir, "ultrasonic":ultra, "timestamp": timestamp}

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Ubidots Response:", response.text)
    except Exception as e:
        print("Error sending to Ubidots:", e)
        
@app.route('/',methods = ['GET'])
def entry_point():
    return jsonify(message="Hello, Mancing mania!")

@app.route('/sensor', methods=['POST'])
def receive_data():
    data = request.json
    if data:
        #Timestamp
        timestamp = datetime.now(UTC).strftime("%d:%m:%Y")
        data["timestamp"] = timestamp
        print(timestamp)
        
        # Simpan ke MongoDB
        collection.insert_one(data)
        
        # Kirim ke Ubidots
        send_to_ubidots(data["temperature"], data["humidity"], data["pir"], data["ultrasonic"], timestamp)
        
        return jsonify({"message": "Data stored and sent to Ubidots successfully", "Timestamp": timestamp}), 201
    return jsonify({"error": "Invalid data"}), 400

@app.route('/sensor', methods=['GET'])
def get_data():
    sensor_data = list(collection.find({}, {"_id": 0}))
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True, port=3000)