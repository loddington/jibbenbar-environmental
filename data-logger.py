from flask import Flask, jsonify, request

# Simple RestAPI for gathering data - Flask is good as a proof of concept but not very robust.
# Not great security. The API Token is passed in plain text over the network. Need to proxy this app behind an SSL server like nginx or apache. 


# You can see what is in the Data logger by using this command:
# curl  -H "Content-Type: application/json"  -X GET http://localhost:5000/sensors

API_KEY = "XXXXXXXX"

sensors = [
    {'id': 'bucket_tips', 'sensor_value': 0},
    {'id': 'probe_temp', 'sensor_value': 0},
]

app = Flask(__name__)

ef authenticate():
    """Authenticate the request using an API key."""
    key = request.headers.get('X-API-Key')
    if key != API_KEY:
        logging.warning("Unauthorized access attempt.")
        abort(401, description="Unauthorized")

@app.errorhandler(401)
def unauthorized(error):
    logging.error(f"401 Unauthorized: {error.description}")
    return jsonify({'error': 'Unauthorized'}), 401

@app.errorhandler(404)
def not_found(error):
    logging.error(f"404 Not Found: {error.description}")
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(400)
def bad_request(error):
    logging.error(f"400 Bad Request: {error.description}")
    return jsonify({'error': 'Bad Request'}), 400

@app.route('/')
def hello_world():
    return 'These are not the droids you are looking for'

@app.route('/sensors', methods=['GET'])
def get_sensors():
    return jsonify({'sensors': sensors})

@app.route('/sensors/<string:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    sensor = [sensor for sensor in sensors if sensor['id'] == sensor_id]
    if len(sensor) == 0:
        return jsonify({'error': 'Sensor not found'})
    return jsonify({'sensor': sensor[0]})


@app.route('/sensors/<string:sensor_id>', methods=['PUT'])
def update_sensors(sensor_id):
    sensor = [sensor for sensor in sensors if sensor['id'] == sensor_id]
    if len(sensor) == 0:
        return jsonify({'error': 'Sensor not found'})
    sensor[0]['sensor_value'] = request.json.get('sensor_value', sensor[0]['sensor_value'])
    return jsonify({'sensor': sensor[0]})



# A new very simple endpoint to increment the sensor_value by 1

@app.route('/sensors/<string:sensor_id>/increment', methods=['PUT'])
def increment_sensor_value(sensor_id):
    sensor = [sensor for sensor in sensors if sensor['id'] == sensor_id]
    if len(sensor) == 0:
        return jsonify({'error': 'Sensor not found'})

    sensor[0]['sensor_value'] = int(sensor[0]['sensor_value']) + 1  
    return jsonify({'sensor': sensor[0]})



if __name__ == '__main__':
   # app.run(debug=False, port=5000)
   app.run(host='0.0.0.0',debug=False, port=5000) # Allow connections on external interfaces - consider the security implications of this. 
