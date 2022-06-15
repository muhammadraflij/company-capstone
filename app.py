from flask import Flask, request
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from weather_colect import weather_by_city, weather_by_location
from weather_list_to_dict import weather_list_to_dict
import pandas as pd

app = Flask(__name__)
  
# load model
model = load_model("Model\lstm_6_3_e50\my_model_weather (1).h5")

@app.route("/")
def index():
  return "Welcome to Airmonitor Weather Forecast APIs"

# /w_by_city?city=Jakarta&key=a98a87d5120e4a86ba63d4c67fe8e81f
@app.route("/w_by_city")
def w_by_city():
  kota = request.args.get('city', default = "Jakarta", type = str)
  weatherbit_key = request.args.get('key', default = "a98a87d5120e4a86ba63d4c67fe8e81f", type = str)

  # collect data
  a = weather_by_city(kota, weatherbit_key)
  a = a.sort_index()

  # scaling and reshape
  scaler = MinMaxScaler()
  data = scaler.fit_transform(a)
  data = data.reshape(1,3,3)

  # predictions and dataframing
  predictions = model.predict(data)
  predictions = predictions.reshape(3,3)
  predictions = scaler.inverse_transform(predictions)
  predictions = predictions.tolist()
  predictions = pd.DataFrame(predictions)
  predictions = predictions.rename(columns={0: "rh", 1: "wind_spd", 2: "temp"})

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
  result_pred = result_pred.sort_index(ascending=False)
  result_pred = result_pred.values.tolist()
  result_pred = weather_list_to_dict(result_pred)

  # data history for return
  result_hist = df_merge[3:6]
  result_hist = result_hist.values.tolist()
  result_hist = weather_list_to_dict(result_hist)
  a = a.sort_index()

  # merge result_pred and result_hist to dict data
  data = ({
      "data": ({
          "forecast": result_pred,
          "history": result_hist
      })
  })
  return data
   
  

# /w_by_location?lat=35&lon=-78&key=8ad9eca88a2e4330a022ad816a7d9886
@app.route("/w_by_location")
def w_by_location():
  lat = request.args.get('lat', default = 35, type = float)
  lon = request.args.get('lon', default = -78, type = float)
  weatherbit_key = request.args.get('key', default = "8ad9eca88a2e4330a022ad816a7d9886", type = str)

  # collect data
  a = weather_by_location(lat, lon, weatherbit_key)
  a = a.sort_index()

  # scaling and reshape
  scaler = MinMaxScaler()
  data = scaler.fit_transform(a)
  data = data.reshape(1,3,3)

  # predictions and dataframing
  predictions = model.predict(data)
  predictions = predictions.reshape(3,3)
  predictions = scaler.inverse_transform(predictions)
  predictions = predictions.tolist()
  predictions = pd.DataFrame(predictions)
  predictions = predictions.rename(columns={0: "rh", 1: "wind_spd", 2: "temp"})

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
  result_pred = result_pred.sort_index(ascending=False)
  result_pred = result_pred.values.tolist()
  result_pred = weather_list_to_dict(result_pred)

  # data history for return
  result_hist = df_merge[3:6]
  result_hist = result_hist.values.tolist()
  result_hist = weather_list_to_dict(result_hist)
  a = a.sort_index()

  # merge result_pred and result_hist to dict data
  data = ({
      "data": ({
          "forecast": result_pred,
          "history": result_hist
      })
  })
  return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
