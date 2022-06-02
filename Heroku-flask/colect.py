import requests
import json
import pandas as pd
from glom import glom

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
            'datetime' : (['datetime']),
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
    new = df["datetime"].str.split(":", n = 1, expand = True)
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
            'datetime' : (['datetime']),
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
    new = df["datetime"].str.split(":", n = 1, expand = True)
    df["date"]= new[0]
    df["time"]= new[1]
    df['datetime'] = df.date.map(str) + " " + df.time
    df = df.drop(['date', 'time'], axis=1)
    df.datetime = pd.to_datetime(df.datetime)
    df = df.set_index('datetime')
    
    # get last datetime
    df = df[:6]   
    
    return df