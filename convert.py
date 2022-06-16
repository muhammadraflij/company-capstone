#convert aqi to ispu
from glom import glom
import json
import pandas as pd
import numpy as np
from numpy import array   
    
def convert_ISPU(predictions):
  for i in range(0, len(predictions)):
    q1 = predictions.pm10.iloc[i] #pm10
    if q1 > 420 :
      k, t , r = (q1 - 420),(500 - 420), (400 - 300)
      ISPU_pm10 = (r*k/t) + 300
    elif 350 < q1 <= 420 :
      k, t , r = (q1 - 350),(420 - 350), (300 - 200)
      ISPU_pm10 = (r*k/t) + 200
    elif 150 < q1 <= 350 :
      k, t , r = (q1 - 150),(350 - 150), (200 - 100)
      ISPU_pm10 = (r*k/t) + 100
    else :
      k, t , r = (q1 - 50),(150 - 50), (100 - 50)
      ISPU_pm10 = (r*k/t) + 50
    q2 = predictions.pm25.iloc[i] #pm2,5
    if q2 > 250.4 :
      k, t , r = (q2 - 250.4),(500 - 250.4), (400 - 300)
      ISPU_pm25 = (r*k/t) + 300
    elif 150.4 < q2 <= 250.4 : 
      k, t , r = (q2 - 150.4),(250.4 - 150.4), (300 - 200)
      ISPU_pm25 = (r*k/t) + 200
    elif 55.4 < q2 <= 150.4 :
      k, t , r = (q2 - 55.4),(150.4 - 55.4), (200 - 100)
      ISPU_pm25 = (r*k/t) + 100
    else :
      k, t , r = (q2 - 15.5),(55.4 - 15.5), (100 - 50)
      ISPU_pm25 = (r*k/t) + 50
    q3 = predictions.o3.iloc[i] #o3
    if q3 > 800:
      k, t , r = (q3 - 800),(1000 - 800), (400 - 300)
      ISPU_o3 = (r*k/t) + 300
    elif 400 < q3 <= 800 : 
      k, t , r = (q3 - 400),(800 - 400), (300 - 200)
      ISPU_o3 = (r*k/t) + 200
    elif 235 < q3 <= 400 :
      k, t , r = (q3 - 235),(400 - 235), (200 - 100)
      ISPU_o3 = (r*k/t) + 100
    else :
      k, t , r = (q3 - 120),(235 - 120), (100 - 50)
      ISPU_o3 = (r*k/t) + 50 
    q4 = predictions.so2.iloc[i] #so2
    if q4 > 800:
      k, t , r = (q4 - 800),(1200 - 800), (400 - 300)
      ISPU_so2 = (r*k/t) + 300
    elif 400 < q4 <= 800 : 
      k, t , r = (q4 - 400),(800 - 400), (300 - 200)
      ISPU_so2 = (r*k/t) + 200
    elif 180 < q4 <= 400 :
      k, t , r = (q4 - 180),(400 - 180), (200 - 100)
      ISPU_so2 = (r*k/t) + 100
    else :
      k, t , r = (q4 - 52),(180 - 52), (100 - 50)
      ISPU_so2 = (r*k/t) + 50
    q5 = predictions.no2.iloc[i] #no2
    if q5 > 2260 :
      k, t , r = (q5 - 2260),(3000 - 2260), (400 - 300)
      ISPU_no2 = (r*k/t) + 300
    elif 1130 < q5 <= 2260 : 
      k, t , r = (q5 - 1130),(2260 - 1130), (300 - 200)
      ISPU_no2 = (r*k/t) + 200
    elif 200 < q5 <= 1130 :
      k, t , r = (q5 - 200),(1130 - 200), (200 - 100)
      ISPU_no2 = (r*k/t) + 100
    else:  
      k, t , r = (q5 - 80),(235 - 80), (100 - 50)
      ISPU_no2 = (r*k/t) + 50
    q6 = predictions.co.iloc[i] #co 
    if q6 > 30000 :
      k, t , r = (q6 - 30000),(45000 - 30000), (400 - 300)
      ISPU_co = (r*k/t) + 300
    elif 15000 < q6 <= 30000 : 
      k, t , r = (q6 - 15000),(30000 - 15000), (300 - 200)
      ISPU_co = (r*k/t) + 200
    elif 8000 < q6 <= 15000 :
      k, t , r = (q6 - 8000),(15000 - 8000), (200 - 100)
      ISPU_co = (r*k/t) + 100
    else :
      k, t , r = (q6 - 4000),(8000 - 4000), (100 - 50)
      ISPU_co = (r*k/t) + 50
    maks = [ISPU_co, ISPU_o3, ISPU_pm25, ISPU_pm10, ISPU_no2, ISPU_so2]
    max_value = None
    for num in maks:
      if (max_value is None or num > max_value):
        max_value = num
    predictions.aqi.iloc[i] = round(max_value)
  return predictions
