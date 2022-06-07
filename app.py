from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from colect import data_by_city, data_by_location, current_aqi_prov
from list_to_dict import list_to_dict, list_to_dict_prov
import pandas as pd

app = Flask(__name__)
  
# load model
model = load_model("Model/lstm_6_3_e50/my_model.h5")

@app.route("/")
def index():
  return "Welcome to Airmonitor Forecast APIs"

# /by_city?city=Jakarta&key=8ad9eca88a2e4330a022ad816a7d9886
@app.route("/by_city")
def by_city():
  kota = request.args.get('city', default = "Jakarta", type = str)
  weatherbit_key = request.args.get('key', default = "8ad9eca88a2e4330a022ad816a7d9886", type = str)

  # collect data
  a = data_by_city(kota, weatherbit_key)
  a = a.sort_index()

  # scaling and reshape
  scaler = MinMaxScaler()
  data = scaler.fit_transform(a)
  data = data.reshape(1,6,7)

  # predictions and dataframing
  predictions = model.predict(data)
  predictions = predictions.reshape(3,7)
  predictions = scaler.inverse_transform(predictions)
  predictions = predictions.tolist()
  predictions = pd.DataFrame(predictions)
  predictions = predictions.rename(columns={0: "aqi", 1: "pm10", 2: "pm25", 
                                          3: "o3", 4: "so2", 
                                          5: "no2", 6: "co"})

  # merge data a and predictions
  frame = [a, predictions]
  df_merge = pd.concat(frame)
  df_merge.index = pd.date_range(df_merge.index[0], periods=len(df_merge), freq='1h')
  df_merge = df_merge.sort_index(ascending=False)

  # reset index and format datetime to obj
  df_merge = df_merge.reset_index()
  df_merge['index'] = df_merge['index'].dt.strftime('%Y-%m-%d %H:%M:%S')

  # data prediction for return
  result_pred = df_merge[:3]
  result_pred = result_pred.values.tolist()
  result_pred = list_to_dict(result_pred)

  # data history for return
  result_hist = df_merge[3:]
  result_hist = result_hist.values.tolist()
  result_hist = list_to_dict(result_hist)

  # merge result_pred and result_hist to dict data
  data = ({
      "data": ({
          "forecast": result_pred,
          "history": result_hist
      })
  })

   
  return data

# /by_location?lat=35&lon=-78&key=8ad9eca88a2e4330a022ad816a7d9886
@app.route("/by_location")
def by_location():
  lat = request.args.get('lat', default = 35, type = float)
  lon = request.args.get('lon', default = -78, type = float)
  weatherbit_key = request.args.get('key', default = "8ad9eca88a2e4330a022ad816a7d9886", type = str)

  # collect data
  a = data_by_location(lat, lon, weatherbit_key)

  # scaling and reshape
  scaler = MinMaxScaler()
  data = scaler.fit_transform(a)
  data = data.reshape(1,6,7)

  # predictions and dataframing
  predictions = model.predict(data)
  predictions = predictions.reshape(3,7)
  predictions = scaler.inverse_transform(predictions)
  predictions = predictions.tolist()
  predictions = pd.DataFrame(predictions)
  predictions = predictions.rename(columns={0: "aqi", 1: "pm10", 2: "pm25", 
                                          3: "o3", 4: "so2", 
                                          5: "no2", 6: "co"})

  # merge data a and predictions
  frame = [a, predictions]
  df_merge = pd.concat(frame)
  df_merge.index = pd.date_range(df_merge.index[0], periods=len(df_merge), freq='1h')
  df_merge = df_merge.sort_index(ascending=False)

  # reset index and format datetime to obj
  df_merge = df_merge.reset_index()
  df_merge['index'] = df_merge['index'].dt.strftime('%Y-%m-%d %H:%M:%S')

  # data prediction for return
  result_pred = df_merge[:3]
  result_pred = result_pred.values.tolist()
  result_pred = list_to_dict(result_pred)

  # data history for return
  result_hist = df_merge[3:]
  result_hist = result_hist.values.tolist()
  result_hist = list_to_dict(result_hist)

  # merge result_pred and result_hist to dict data
  data = ({
      "data": ({
          "forecast": result_pred,
          "history": result_hist
      })
  })
    
  return data

# /current?key=8ad9eca88a2e4330a022ad816a7d9886
@app.route("/current")
def current():
  weatherbit_key = request.args.get('key', default = "8ad9eca88a2e4330a022ad816a7d9886", type = str)

  data = current_aqi_prov(weatherbit_key)
  data = list_to_dict_prov(data)
  
  data = ({
      "data": ({
          "current": data
      })
  })
  
  return data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
