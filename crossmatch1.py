#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 23:04:51 2020

@author: kushasahu
"""


# Write your import_bss function here.
import numpy as np;
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
    r1 = np.radians(ra1)
    r2 = np.radians(ra2)
    d1 = np.radians(dec1)
    d2 = np.radians(dec2)
    
    b = np.cos(d1)*np.cos(d2)*np.sin(np.abs(r1 - r2)/2)**2
    a= np.sin(np.abs(d1 - d2)/2)**2
    d = 2*np.arcsin(np.sqrt(a + b))
    return np.degrees(d);

def find_closest (data, ra, dec, maxDist) :
    minUptilNow = 1000;
    selectedId = -1;
    for i, r in enumerate(data, 1) :
        dist = angular_dist(r[1], r[2], ra, dec);
        if dist < minUptilNow and dist < maxDist:
            minUptilNow = dist;
            selectedId = r[0]
    return (selectedId, minUptilNow);
 

def crossmatch (data1, data2, maxDist) : 
    matches = []
    noMatches = []
    for i, r in enumerate(data1, 1):
        cId, cD = find_closest(data2, r[1], r[2], maxDist);
        if cId == -1 :
            noMatches.append(i);
        else:
            matches.append((i, cId, cD));
    return matches, noMatches;
    
    
if __name__ == '__main__':
  # Output of the import_bss and import_super functions
  bss_cat = import_bss()
  super_cat = import_super()
  print(bss_cat)
  print(super_cat)