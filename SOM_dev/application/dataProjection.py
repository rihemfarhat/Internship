#!/usr/bin/env python
from SOMTools import *
import np as np
import pickle
import ConfigParser
import sys
import itertools

configFileName = sys.argv[1]
Config = ConfigParser.ConfigParser()
Config.read(configFileName)

infile = Config.get('dataProjection', 'dataFile')
outFileName = Config.get('dataProjection', 'outFileName')
bmuFileName = Config.get('dataProjection', 'bmuFileName')
smap = Config.get('dataProjection', 'map')
vmin = Config.get('dataProjection', 'vmin')
vmax = Config.get('dataProjection', 'vmax')
try:
 vmin = float(vmin)
except ValueError:
 vmin = None
try:
 vmax = float(vmax)
except ValueError:
 vmax = None
smap = np.load(smap)
X,Y,Z,cardinal = smap.shape
dataMap = np.zeros((X,Y,Z))
data = np.genfromtxt(infile)
idata = itertools.chain(data)
bmuCoordinates = np.load(bmuFileName)
if data.shape[0] == bmuCoordinates.shape[0]:
 density = np.zeros((X,Y,Z))
 for bmu in bmuCoordinates:
  i,j,k = bmu
  dataMap[i,j,k] += idata.next()
  density[i,j,k] += 1
 dataMap = dataMap / density
 pickle.dump(dataMap, open('%s.dat'%outFileName, 'w'))
 flatten_map = np.concatenate((smap.reshape(X*Y*Z,cardinal), np.atleast_2d(dataMap.reshape(X*Y*Z)).T), axis=1)
 np.savetxt('%s.txt'%outFileName, flatten_map)
else:
 ##updated the syntax of the print function   
    print('Shape mismatch between data ({}) and bmuCoordinates ({})!'.format(data.shape[0], bmuCoordinates.shape[0]))
    


