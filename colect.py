import requests
import json
import pandas as pd
from glom import glom
import datetime

def data_by_city(city,key):    
    # Base URL and api key
    link = "https://api.weatherbit.io/v2.0/history/airquality?"
    api_key = key

    # city variable and req to weatherbit.io
    city = f"city={city}&country=indonesia"
    history_72hour = link + city + "&key=" + api_key
    r = requests.get(history_72hour)

    # Json to Dict
    df = pd.read_json(r.text)
    target = df['data']
    spec = {
            'datetime' : (['timestamp_local']),
            'aqi' : (['aqi']),
            'pm10' : (['pm10']),
            'pm25' : (['pm25']),
            'o3' : (['o3']),
            'so2' : (['so2']),
            'no2' : (['no2']),
            'co' : (['co']),
    }

    data_json = glom(target, spec)

    # Dict to Dataframe
    df = pd.DataFrame.from_dict(data_json)
    
    # format datetime and set to index
    new = df["datetime"].str.split("T", n = 1, expand = True)
    df["date"]= new[0]
    df["time"]= new[1]
    df['datetime'] = df.date.map(str) + " " + df.time
    df = df.drop(['date', 'time'], axis=1)
    df.datetime = pd.to_datetime(df.datetime)
    df = df.set_index('datetime')
    
    # get last datetime
    df = df[:6]   

    return df

def data_by_location(lat,lon,key):    
    # Base URL and api key
    link = "https://api.weatherbit.io/v2.0/history/airquality?"
    api_key = str(key)

    # location variable and req to weatherbit.io
    lat = str(lat)
    lon = str(lon)
    lat_lon = f"lat={lat}&lon={lon}"
    history_72hour = link + lat_lon + "&key=" + api_key
    r = requests.get(history_72hour)

    # Json to Dict
    df = pd.read_json(r.text)
    target = df['data']
    spec = {
            'datetime' : (['timestamp_local']),
            'aqi' : (['aqi']),
            'pm10' : (['pm10']),
            'pm25' : (['pm25']),
            'o3' : (['o3']),
            'so2' : (['so2']),
            'no2' : (['no2']),
            'co' : (['co']),
    }

    data_json = glom(target, spec)

    # Dict to Dataframe
    df = pd.DataFrame.from_dict(data_json)
    
    # format datetime and set to index
    new = df["datetime"].str.split("T", n = 1, expand = True)
    df["date"]= new[0]
    df["time"]= new[1]
    df['datetime'] = df.date.map(str) + " " + df.time
    df = df.drop(['date', 'time'], axis=1)
    df.datetime = pd.to_datetime(df.datetime)
    df = df.set_index('datetime')
    
    # get last datetime
    df = df[:6]   
    
    return df

def current_aqi_prov(key):
  kota = {
      # serang - samarinda
      "-6.11528": "106.15417", "-6.92222": "107.60694", "-6.99306": "110.42083",
      "-7.24917": "112.7508", "-7.80139": "110.3647", "-8.65": "115.21667",
      "-8.58333": "116.11667", "-10.1708": "123.60694", "-0.03194": "109.325",
      "-3.31987": "114.5908", "-2.20833": "113.91667", "-0.49167": "117.1458",
      # tanjung selor - manokwari
      "2.8375": "117.36528", "-2.68056": "118.88611", "-3.9778": "122.51507",
      "-5.14861": "119.43194", "-0.90833": "119.87083", "1.48218": "124.84892",
      "0.5375": "123.0625 ", "-3.69583": "128.18333", "0.73729": "127.5588",
      "-2.53371": "140.71813", "-0.86291": "134.06402",
      # bengkulu - pangkal pinang
      "-3.57710": "102.36053", "-6.20856": "106.83499", "-1.61112": "103.61570",
      "0.91849": "104.46710", "0.50871": "101.45400", "-0.93492": "100.40323",
      "-2.97313": "104.77291", "3.63781": "98.70642", "-5.39714": "105.26549",
      "5.57007": "95.36970", "-2.12960": "106.10302"
  }

  z = []
  data = []

  for x,y in kota.items():
    api_key = key#"8ad9eca88a2e4330a022ad816a7d9886"
    lat = x

    current = f"https://api.weatherbit.io/v2.0/current/airquality?lat={x}&lon={y}&key={api_key}"
    r = requests.get(current)
    
    df = pd.read_json(r.text)
    target = df["data"]
    spec = {      
        "aqi" : (["aqi"]),
        "pm10" : (["pm10"]),
        "pm25" : (["pm25"]),
        "o3" : (["o3"]),
        "so2" : (["so2"]),
        "no2" : (["no2"]),
        "co" : (["co"])
    }

    data_json = glom(target, spec)
    df_aqi = pd.DataFrame.from_dict(data_json)
    df_city = df[["city_name", "lat", "lon"]]
    df_merge = pd.concat([df_city, df_aqi], axis=1, sort=False)
    df_merge = df_merge.values.tolist()
    z.append(df_merge)

    for x in z:
      for y in x:
        if y not in data:
          data.append(y)
    
  return data

def weather_by_city(city,key):    
    # Base URL and api key
    link = "https://api.weatherbit.io/v2.0/history/hourly?"
    api_key = str(key)
    today = datetime.date.today()
    start = today - datetime.timedelta(days = 1)
    end = today
    # city variable and req to weatherbit.io
    city = f"city={city}&country=indonesia"
    history_72hour = link + city + "&start_date=" + str(start) + "&end_date=" + str(end) + "&tz=local&key=" + api_key
    r = requests.get(history_72hour)
    j = r.json()
    jd = j['data']

    spec = {
            'datetime' : (['datetime']),
            'rh' : (['rh']),
            'wind_spd' : (['wind_spd']),
            'temp' : (['temp']),
    }
    data_json = glom(jd, spec)
    df = pd.DataFrame.from_dict(data_json)
    new = df["datetime"].str.split(":", n = 1, expand = True)
    df["date"]= new[0]
    df["time"]= new[1]
    df['datetime'] = df.date.map(str) + " " + df.time
    df = df.drop(['date', 'time'], axis=1)
    df.datetime = pd.to_datetime(df.datetime)
    df = df.set_index('datetime')
    
    # get last datetime
    df = df[:3]   

    return df

def weather_by_location(lat,lon,key):    
    # Base URL and api key
    link = "https://api.weatherbit.io/v2.0/history/hourly?"
    api_key = str(key)
    today = datetime.date.today()
    start = today - datetime.timedelta(days = 1)
    end = today
    # location variable and req to weatherbit.io
    lat = str(lat)
    lon = str(lon)
    lat_lon = f"lat={lat}&lon={lon}"
    history_72hour = link + lat_lon + "&start_date=" + str(start) + "&end_date=" + str(end) + "&tz=local&key=" + api_key
    r = requests.get(history_72hour)
    j = r.json()
    jd = j['data']

    spec = {
            'datetime' : (['datetime']),
            'rh' : (['rh']),
            'wind_spd' : (['wind_spd']),
            'temp' : (['temp']),
    }
    data_json = glom(jd, spec)
    df = pd.DataFrame.from_dict(data_json)
    new = df["datetime"].str.split(":", n = 1, expand = True)
    df["date"]= new[0]
    df["time"]= new[1]
    df['datetime'] = df.date.map(str) + " " + df.time
    df = df.drop(['date', 'time'], axis=1)
    df.datetime = pd.to_datetime(df.datetime)
    df = df.set_index('datetime')
    
    # get last datetime
    df = df[:3]   

    return df
