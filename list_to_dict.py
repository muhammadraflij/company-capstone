import numpy as np


# format List in list to dict with key
def list_to_dict(lst):
  # format list value to int
  x = lst
  data = []

  for i in range(len(x)):
    item_x = x[i]
    for item in item_x:
      z = {"aqi": item_x[0],
          "pm10": item_x[1],
          "pm25": item_x[2],
          "o3": item_x[3],
          "so2": item_x[4],
          "no2": item_x[5],
          "co": item_x[6]}
    
      if z not in data:
        data.append(z)
        
  return data

# format list to dict for aqi 34 province
def list_to_dict_prov(lst):
  x = lst
  data = []

  for i in range(len(x)):
    item_x = x[i]
    for item in item_x:
      z = {"city": item_x[0],
           "lat": item_x[1],
           "lon": item_x[2],
           "aqi": item_x[3],
           "pm10": item_x[4],
           "pm25": item_x[5],
           "o3": item_x[6],
           "so2": item_x[7],
           "no2": item_x[8],
           "co": item_x[9]}
    
      if z not in data:
        data.append(z)
     
  return data