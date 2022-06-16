#convert aqi to ispu
from glom import glom
import json
import pandas as pd
import numpy as np
from numpy import array   
    
def convert_ISPU(predictions):
  for i in range(0, len(predictions)):
    max_particle = predictions.iloc[i].max()
    q1 = predictions.pm10.iloc[i] #pm10
    q2 = predictions.pm25.iloc[i] #pm2,5
    q3 = predictions.o3.iloc[i] #o3
    q4 = predictions.so2.iloc[i] #so2
    q5 = predictions.no2.iloc[i] #no2
    q6 = predictions.co.iloc[i] #co
    if max_particle == q1: 
      if q1 > 420:
        k, t , r = (q1 - 420),(500 - 420), (400 - 300)
        ISPU = (r*k/t) + 300
      elif 350 < q1 < 420:
        k, t , r = (q1 - 350),(420 - 350), (300 - 200)
        ISPU = (r*k/t) + 200
      elif 150 < q1 < 350:
        k, t , r = (q1 - 150),(350 - 150), (200 - 100)
        ISPU = (r*k/t) + 100
      else :
        k, t , r = (q1 - 50),(150 - 50), (100 - 50)
        ISPU = (r*k/t) + 50
    elif max_particle == q2:
      if q2 > 250.4:
        k, t , r = (q2 - 250.4),(500 - 250.4), (400 - 300)
        ISPU = (r*k/t) + 300
      elif 150.4 < q2 < 250.4: 
        k, t , r = (q2 - 150.4),(250.4 - 150.4), (300 - 200)
        ISPU = (r*k/t) + 200
      elif 55.4 < q2 < 150.4:
        k, t , r = (q2 - 55.4),(150.4 - 55.4), (200 - 100)
        ISPU = (r*k/t) + 100
      else :
        k, t , r = (q2 - 15.5),(55.4 - 15.5), (100 - 50)
        ISPU = (r*k/t) + 50
    elif max_particle == q3:
      if q3 > 800:
        k, t , r = (q3 - 800),(1000 - 800), (400 - 300)
        ISPU = (r*k/t) + 300
      elif 400 < q3 < 800: 
        k, t , r = (q3 - 400),(800 - 400), (300 - 200)
        ISPU = (r*k/t) + 200
      elif 235 < q3 < 400:
        k, t , r = (q3 - 235),(400 - 235), (200 - 100)
        ISPU = (r*k/t) + 100
      else :
        k, t , r = (q3 - 120),(235 - 120), (100 - 50)
        ISPU = (r*k/t) + 50 
    elif max_particle == q4:
      if q4 > 800:
        k, t , r = (q4 - 800),(1200 - 800), (400 - 300)
        ISPU = (r*k/t) + 300
      elif 400< q4 < 800: 
        k, t , r = (q4 - 400),(800 - 400), (300 - 200)
        ISPU = (r*k/t) + 200
      elif 180 < q4 < 400:
        k, t , r = (q4 - 180),(400 - 180), (200 - 100)
        ISPU = (r*k/t) + 100
      else :
        k, t , r = (q4 - 52),(180 - 52), (100 - 50)
        ISPU = (r*k/t) + 50
    elif max_particle == q5:
      if q5 > 2260:
        k, t , r = (q5 - 2260),(3000 - 2260), (400 - 300)
        ISPU = (r*k/t) + 300
      elif 1130 < q5 < 2260: 
        k, t , r = (q5 - 1130),(2260 - 1130), (300 - 200)
        ISPU = (r*k/t) + 200
      elif 200 < q5 < 1130:
        k, t , r = (q5 - 200),(1130 - 200), (200 - 100)
        ISPU = (r*k/t) + 100
      else:  
        k, t , r = (q5 - 80),(235 - 80), (100 - 50)
        ISPU = (r*k/t) + 50
    else : 
      if q6 > 30000:
        k, t , r = (q6 - 30000),(45000 - 30000), (400 - 300)
        ISPU = (r*k/t) + 300
      elif 15000 < q6 < 30000: 
        k, t , r = (q6 - 15000),(30000 - 15000), (300 - 200)
        ISPU = (r*k/t) + 200
      elif 8000 < q6 < 15000:
        k, t , r = (q6 - 8000),(15000 - 8000), (200 - 100)
        ISPU = (r*k/t) + 100
      else :
        k, t , r = (q6 - 4000),(8000 - 4000), (100 - 50)
        ISPU = (r*k/t) + 50
    predictions.aqi.iloc[i] = round(ISPU)
  return predictions
