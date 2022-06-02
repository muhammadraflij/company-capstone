import numpy as np

# format List in list to dict with key
def list_to_dict(lst):
  x = list(np.int_(lst))
  data = {}

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
      data[i] = z
  return data