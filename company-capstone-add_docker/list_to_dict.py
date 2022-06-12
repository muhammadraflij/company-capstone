import numpy as np


# format List in list to dict with key
def list_to_dict(lst):
  # format list value to int
  x = lst
  data = []

  for i in range(len(x)):
    item_x = x[i]
    for item in item_x:
      z = {"rh": item_x[0],
          "wind_spd": item_x[1],
          "temp": item_x[2],}
    
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
           "rh": item_x[3],
           "wind_spd": item_x[4],
           "temp": item_x[5]}
    
      if z not in data:
        data.append(z)
     
  return data