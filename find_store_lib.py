import math
import googlemaps
import os
import csv

from datetime import datetime


def calculate_distance(lat1, lon1, lat2, lon2):
  # naive version: you get distance in "degrees", but issue with earth's curvature
  # dist = math.sqrt(abs((lon1 - lon2)**2 + (lat1 - lat2)**2))
  # return dist

  # Go with a great circle solution.
  earthRadiusKm = 6371;

  # convert to radians
  dLat = math.radians(lat2-lat1);
  dLon = math.radians(lon2-lon1);

  lat1 = math.radians(lat1);
  lat2 = math.radians(lat2);

  # use haversine formula
  a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)); 
  distance = earthRadiusKm * c;
  return distance

def find_closest(f_lat,f_long):
  f = open("sorted-store-locations.csv", "r")
  dy  = 100
  closest = None
  # This is a naive brute force solution. The ideal solution would be
  # a k-d tree.
  for line in f:
    data = line.split(",")
    cur_lat = data[0]
    cur_long = data[1]
    ldist = calculate_distance(float(cur_lat), float(cur_long), float(f_lat), float(f_long))
    if ldist < dy:
      dy = ldist
      closest = line

  data = list(csv.reader([closest]))
  data = data[0]
  data.append(dy)
  f.close()
  return(data)  

def find_store(address):
  
  gmaps = googlemaps.Client(key=os.environ['GROVECO_GOOGLE_API_KEY'])

  # Geocoding an address
  geocode_result = gmaps.geocode(address)
  coords = geocode_result[0]['geometry']['location']
  result = find_closest(coords['lat'],coords['lng'])
  closest = [result[4],result[5],result[6],result[7],result[9]]
  return closest
 
