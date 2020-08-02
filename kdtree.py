#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 18:52:20 2020

@author: kushasahu
"""
import numpy as np;
import math;
import time;

def hms2dec (d,m,s):
  return (15*(d+ m/60 + s/(60*60)));

def dms2dec (d, am, asec):
  signMultiplier = 1 if (d>=0 ) else -1;
  return (signMultiplier* (abs(d) + am/60 + asec/(60*60)))

def import_bss ():
  cat = np.loadtxt('bss3.dat', usecols=range(1, 7));
  final = [];
  for i, r in enumerate(cat,1) :
    final.append([hms2dec(r[0],r[1],r[2]), dms2dec(r[3],r[4],r[5])]);
  return final;

def import_super():
  cat = np.loadtxt('cosmos.csv', delimiter=',', skiprows=1, usecols=[0, 1])
  final = [];
  for i, r in enumerate(cat,1) :
    final.append([r[0], r[1]]);
  return final;

class Node():
    def __init__(self, val, left, right):
        self.val = val
        self.right = right;
        self.left = left;
    
class KDTree():
    def __init__(self, pointList):
        def build(pointList, depth, noOfDimensions):
            #print("pointList", pointList)
            if pointList is None or len(pointList) <= 0 :
                return None;
            
            axis = depth % noOfDimensions;
            #print(depth, noOfDimensions, axis)
            pointList  = sorted(pointList, key = lambda point:point[axis])
            #print("pointList after sort", pointList)
            median = math.floor(len(pointList)/2);
            #print("median", median)
            node = Node(val = pointList[median], 
                        left = build(pointList[0:median],depth+1, noOfDimensions),
                        right = build(pointList[median+1:], depth+1, noOfDimensions));
            #print("axis, node", axis, node.val)
            return node;
        self.root = build(pointList, 0, len(pointList[0]));
    
    def contructTree(points): 
        #print("pointList", points)
        tree = KDTree(points);
        #print("tree", tree)
        return tree;
 
# def getDistance (p1, p2):
#     x1,y1 = p1;
#     x2,y2 = p2;
    
#     x = x1-x2;
#     y = y1-y2;
 

#     return math.sqrt(x*x + y*y); 

def getDistance (p1, p2) : #angular dist     
    ra1, dec1 = p1
    ra2, dec2 = p2
    b = np.cos(dec1)*np.cos(dec2)*np.sin(np.abs(ra1 - ra2)/2)**2
    a= np.sin(np.abs(dec1 - dec2)/2)**2
    d = 2*np.arcsin(np.sqrt(a + b))
    return np.degrees(d);

def compareAndGetClosesPoint (point, p1, p2) :
    if p1 is None :
        return p2;
    if p2 is None :
        return p1;
    
    d1 = getDistance(point, p1);
    d2 = getDistance(point, p2);
    
    if (d1 <= d2):
        return p1;
    else :
        return p2;
    

def getClosestPoint(point, root, depth, k) :
    if root is None :
        return None;
    
    axis = depth % k;
    
    subtree = None;
    oppositeSubtree = None;
    if(point[axis] < root.val[axis]) :
        subtree = root.left;
        oppositeSubtree = root.right;
    else :
        subtree = root.right;
        oppositeSubtree = root.left;
        
    best = compareAndGetClosesPoint(point, 
                                    getClosestPoint(
                                        point, 
                                        subtree, depth+1,
                                        k), root.val);
    bestDistance = getDistance(point, best);
    distanceToWall = abs(point[axis] - root.val[axis]);
    #print("best till now:", best, bestDistance, distanceToWall)
    
    if ( bestDistance > distanceToWall):
        
        best = compareAndGetClosesPoint(point, 
                                    getClosestPoint(
                                        point, 
                                        oppositeSubtree, depth+1,
                                        k), best);
    
    return best;
        
def matchCatalogs (data1, data2, maxDistance): 
    start = time.perf_counter()
    cat1 = np.radians(data1)
    cat2 = np.radians(data2)
    
    treeForCatalog2 = KDTree.contructTree(cat2);
    root = treeForCatalog2.root;
    k = len(cat1[0]);
    
    matches = []
    noMatches = []
    
    for point in cat1:
        best = getClosestPoint(point, root, 0, k);
        dist = getDistance(point, best);
        pDeg = np.degrees(point)
        bestDeg = np.degrees(best);
        if dist > maxDistance:
            noMatches.append(pDeg)
        else :
            matches.append([pDeg, bestDeg])
    diff = time.perf_counter() - start
    return matches, noMatches, diff;

def printTree(root):
    if root is None:
        return;
    print(root.val)
    printTree(root.left)
    printTree(root.right)
    
    
if __name__ == '__main__':
    # pointList = np.array([[3,6], [17,15], [13,15], [6,12], [9,1], [2,6], [10,19]]);

    # tree = KDTree.contructTree(pointList);
    # root = tree.root
    # printTree(tree.root)
    
    # closest = getClosestPoint([15,15], root, 0, 2)
    # print("closest:", closest)
    cat1 = import_bss()
    print("searching for ", len(cat1), "objects")
    cat2 = import_super()
    print("searching in ", len(cat2), "objects")
    #print(cat1)
    matches, noMatches, timeTaken = matchCatalogs(cat1, cat2, 40/3600)
    print("matched", len(matches), "objects")
    print("matches:",matches)
    print("______________________________________________________")
    print("noMatches:",noMatches)
    print("______________________________________________________")
    print("timeTaken:",timeTaken)
    
            