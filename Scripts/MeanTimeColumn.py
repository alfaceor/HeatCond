#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
parser.add_option("-x", "--xcolumn", dest="xcolumn")
parser.add_option("-y", "--ycolumn", dest="ycolumn")
parser.add_option("-X", "--Xlabel", dest="Xlabel")
parser.add_option("-Y", "--Ylabel", dest="Ylabel")
parser.add_option("-t", "--transient", dest="transient")

(options, args) = parser.parse_args()

if options.xcolumn == None:
  xcolumn = 0
else:
  xcolumn = int(options.xcolumn)

if options.ycolumn == None:
  ycolumn = 1
else:
  ycolumn = int(options.ycolumn)
  
if options.transient == None:
  transient = 200
else:
  transient = int(options.transient)

N=40
deltaT=0.2
filename = args
for i in range(len(filename)):
  data=np.loadtxt(filename[i])
  dataKol = data[transient:,xcolumn]
  kolMean = dataKol.mean()
  kolVar  = dataKol.var()
  kolKurt = ((dataKol - kolMean)**4).mean()/(kolVar**2)
  print kolMean, kolMean*N/deltaT, kolVar, kolKurt
  
