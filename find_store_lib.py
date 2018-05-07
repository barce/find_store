import math
import googlemaps
import os
import os.path
import csv
import _pickle as cPickle

from datetime import datetime



def distance(point1, point2):
  # Go with a great circle solution.
  earthRadiusKm = 6371;

  lat1 = float(point1[0])
  lon1 = float(point1[1])

  lat2 = float(point2[0])
  lon2 = float(point2[1])

  # convert to radians
  dLat = math.radians(lat2-lat1);
  dLon = math.radians(lon2-lon1);

  lat1 = math.radians(lat1);
  lat2 = math.radians(lat2);

  # use haversine formula
  a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)); 
  dist_km = earthRadiusKm * c;
  return dist_km

# f = open("myTweets.pickle", "wb")
# cPickle.dump(tweets, f)
# f.close

def extract_transform_load(filename):
  counter = 0
  point_list = []
  with open(filename) as csvfile:
    reader = csv.reader(csvfile) 
    for row in reader:
      if counter > 0:
        point_list.append((float(row[6]),float(row[7])))
      counter += 1

  kd_tree = KDTree(point_list)
  f = open("kd_tree.pickle", "wb")
  cPickle.dump(kd_tree, f)
  f.close

  # binary tree
  return True

def find_closest(f_lat,f_long):
  data_file = "store-locations.csv"
  pickle_file = "kd_tree.pickle"
    
  if os.path.isfile(pickle_file) != True:
    extract_transform_load(data_file)

  # load tree
  kd_tree = cPickle.load(open(pickle_file, "rb"))
  results = kd_tree.closest_point((f_lat,f_long))

  with open(data_file) as csvfile:
    reader = csv.reader(csvfile) 
    for row in reader:
      try: 
        if float(row[6]) == results[0] and float(row[7]) == results[1]:
          dist = distance((f_lat,f_long),results)
          row.append(dist)
          return(row)
      except:
        i = 0

def find_store(address):
  
  gmaps = googlemaps.Client(key=os.environ['GROVECO_GOOGLE_API_KEY'])

  # Geocoding an address
  geocode_result = gmaps.geocode(address)
  coords = geocode_result[0]['geometry']['location']
  result = find_closest(float(coords['lat']),float(coords['lng']))
  closest = result
  return closest
 

class KDTree(object):
  """
  kd-tree spatial index and nearest neighbour search
  """
  
  def __init__(self, point_list, _depth=0):
    if point_list:
      # Select axis based on depth so that axis cycles through all valid values
      self.axis = _depth % len(point_list[0])
               
      # Sort point list and choose median as pivot element
      point_list = sorted(point_list, key=lambda point: point[self.axis])
      median = len(point_list) // 2 # choose median

      # Create node and construct subtrees
      self.location = point_list[median]
      self.child_left = KDTree(point_list[:median], _depth + 1)
      self.child_right = KDTree(point_list[median + 1:], _depth + 1)
    else:
      self.axis = 0
      self.location = None
      self.child_left = None
      self.child_right = None

  def closest_point(self, point, _best=None):
    if self.location is None:
      return _best
 
    if _best is None:
      _best = self.location
 
    # consider the current node
    if distance(self.location, point) < distance(_best, point):
      _best = self.location
 
    # search the near branch
    _best = self._child_near(point).closest_point(point, _best)
 
    # search the away branch - maybe
    if self._distance_axis(point) < distance(_best, point):
      _best = self._child_away(point).closest_point(point, _best)
 
    return _best

  # internal methods
  
  def __repr__(self):
    """
    Simple representation for doctests
    """
    if self.location:
      return "(%d, %s, %s, %s)" % (self.axis, repr(self.location), repr(self.child_left), repr(self.child_right))
    else:
      return "None"

  def _distance_axis(self, point):
    # project point onto node axis
    # i.e. want to measure distance on axis orthogonal to current node's axis
    axis_point = list(point)
    axis_point[self.axis] = self.location[self.axis]
    return distance(tuple(axis_point), point)

  def _child_near(self, point):
    """
    Either left or right child, whichever is closest to the point
    """
    if point[self.axis] < self.location[self.axis]:
      return self.child_left
    else:
      return self.child_right

  def _child_away(self, point):
    """
    Either left or right child, whichever is furthest from the point
    """
    if self._child_near(point) is self.child_left:
      return self.child_right
    else:
      return self.child_left  


