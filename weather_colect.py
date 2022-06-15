import requests
import json
import pandas as pd
from glom import glom
import datetime

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