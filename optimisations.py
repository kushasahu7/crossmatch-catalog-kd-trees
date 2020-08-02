# Write your crossmatch function here.
import numpy as np
import time;

def hms2dec (d,m,s):
  return (15*(d+ m/60 + s/(60*60)));

def dms2dec (d, am, asec):
  signMultiplier = 1 if (d>=0 ) else -1;
  return (signMultiplier* (abs(d) + am/60 + asec/(60*60)))

def import_bss ():
  cat = np.loadtxt('bss.dat', usecols=range(1, 7));
  final = [];
  for i, r in enumerate(cat,1) :
    final.append((i, hms2dec(r[0],r[1],r[2]), dms2dec(r[3],r[4],r[5])));
  return final;

def import_super():
  cat = np.loadtxt('super.csv', delimiter=',', skiprows=1, usecols=[0, 1])
  final = [];
  for i, r in enumerate(cat,1) :
    final.append((i, r[0], r[1]));
  return final;
  
def angular_dist (ra1, dec1, ra2, dec2) :     
    b = np.cos(dec1)*np.cos(dec2)*np.sin(np.abs(ra1 - ra2)/2)**2
    a= np.sin(np.abs(dec1 - dec2)/2)**2
    d = 2*np.arcsin(np.sqrt(a + b))
    return d;

def find_closest (data, ra, dec, maxDist) :
    ra2s = data[:,0];
    dec2s = data[:,1];
    distList = angular_dist(ra, dec, ra2s, dec2s);
    minDist = np.degrees(np.min(distList));
    if(minDist < maxDist):
        selectedId = np.argmin(distList)
        return (selectedId, minDist)
    
    return (-1, np.inf);
 

def crossmatch (cat1, cat2, maxDist) : 
    matches = []
    noMatches = []
    data1 = np.radians(cat1)
    data2 = np.radians(cat2)
    start = time.perf_counter()
    #print("data1", data1)
    for i, r in enumerate(data1, 0):
        #print("r", r)
        cId, cD = find_closest(data2, r[0], r[1], maxDist);
        if cId == -1 :
            noMatches.append(i);
        else:
            matches.append((i, cId, cD));
    end = time.perf_counter() - start
    return matches, noMatches, end;



# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  # The example in the question
  ra1, dec1 = np.radians([180, 30])
  cat2 = [[180, 32], [55, 10], [302, -44]]
  cat2 = np.radians(cat2)
  ra2s, dec2s = cat2[:,0], cat2[:,1]
  print(ra1, dec1)
  print(ra2s, dec2s)
  dists = angular_dist(ra1, dec1, ra2s, dec2s)
  print(np.degrees(dists))

  cat1 = np.array([[180, 30], [45, 10], [300, -45]])
  cat2 = np.array([[180, 32], [55, 10], [302, -44]])
  matches, no_matches, time_taken = crossmatch(cat1, cat2, 5)
  print('matches:', matches)
  print('unmatched:', no_matches)
  print('time taken:', time_taken)
    
    # A function to create a random catalogue of size n
  def create_cat(n):
      ras = np.random.uniform(0, 360, size=(n, 1))
      decs = np.random.uniform(-90, 90, size=(n, 1))
      return np.hstack((ras, decs))
    
    # Test your function on random inputs
  np.random.seed(0)
  cat1 = create_cat(10)
  cat2 = create_cat(20)
  matches, no_matches, time_taken = crossmatch(cat1, cat2, 5)
  print('matches:', matches)
  print('unmatched:', no_matches)
  print('time taken:', time_taken)
