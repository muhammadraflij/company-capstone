from flask import Flask, request, jsonify
#from flask_ngrok import run_with_ngrok
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from colect import data_by_city, data_by_location
from list_to_dict import list_to_dict

#!ngrok authtoken "29mT8kj4OLsAwQwkFiaePr4CQ10_6QbJzAjNwjjSr9cTdWP8h"

app = Flask(__name__)
#run_with_ngrok(app)   

# load model
model = load_model("Model/lstm_6_3_e50/my_model.h5")

@app.route("/")
def index():
  return "Welcome to Airmonitor Forecast APIs"

# /by_city?city=Jakarta&key=
@app.route("/by_city")
def by_city():
  kota = request.args.get('city', default = "Jakarta", type = str)
  weatherbit_key = request.args.get('key', default = "9308fac32c9d45a8a4ba9dc418df799f", type = str)
  # collect data
  a = data_by_city(kota, weatherbit_key)

  # scaling and reshape
  scaler = MinMaxScaler()
  data = scaler.fit_transform(a)
  data = data.reshape(1,6,7)

  # predictions
  predictions = model.predict(data)
  predictions = predictions.reshape(3,7)
  predictions = scaler.inverse_transform(predictions)
  predictions = predictions.tolist()
  
  return jsonify(predictions)
  #return f"forecast for the next 3 hours in {kota} \n\n\n {predictions}"

# /by_location?lat=35&lon=-78&key=
@app.route("/by_location")
def by_location():
  lat = request.args.get('lat', default = 35, type = float)
  lon = request.args.get('lon', default = -78, type = float)
  weatherbit_key = request.args.get('key', default = "9308fac32c9d45a8a4ba9dc418df799f", type = str)
  # collect data
  a = data_by_location(lat, lon, weatherbit_key)

  # scaling and reshape
  scaler = MinMaxScaler()
  data = scaler.fit_transform(a)
  data = data.reshape(1,6,7)

  # predictions
  predictions = model.predict(data)
  predictions = predictions.reshape(3,7)
  predictions = scaler.inverse_transform(predictions)
  predictions = predictions.tolist()

  return jsonify(predictions)
  #return f"forecast for the next 3 hours in {lat}, {lon} \n\n\n {predictions}"



if __name__ == "__main__":
    app.run(debug=True)