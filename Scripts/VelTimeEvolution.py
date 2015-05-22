#!/usr/bin/python -i

# TODO: Calculate mean value between realizations (experiments or trials) for the .dat files

import numpy as np
import matplotlib.pyplot as plt

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
parser.add_option("-M", "--Mfiles", dest="Mfiles")
parser.add_option("-o", "--outfilename", dest="outfilename")

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
#parser.add_option("-k", "--kmcolumn", dest="kmcolumn")

(options, args) = parser.parse_args()

font = {'family' : 'normal',
         'weight' : 'bold',
         'size'   : 30}
plt.rc('font', **font)
plt.rc('text', usetex=True)

filename=args
Mfiles=len(args)
k=40
for i in range(Mfiles):
  ttime, vel =np.loadtxt(filename[i], usecols=(0,2*k-1)).T
  print vel
  plt.plot(ttime, vel,'o-') # First particle vel.


plt.xlim(0,3000)
plt.ylim(-5,5)
plt.ylabel("$\\omega_{"+str(k)+"}$")
plt.xlabel("$t$")  
plt.show()
