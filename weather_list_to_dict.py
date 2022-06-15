import numpy as np


# format List in list to dict with key
def weather_list_to_dict(lst):
  # format list value to int
  x = lst
  data = []

  for i in range(len(x)):
    item_x = x[i]
    for item in item_x:
      z = {"datetime" : item_x[0],
          "rh": item_x[1],
          "wind_spd": item_x[2],
          "temp": item_x[3],}
    
      if z not in data:
        data.append(z)
        
  return data