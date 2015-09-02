#!/usr/bin/python

import numpy as np

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
parser.add_option("-M", "--Mfiles", dest="Mfiles")
#parser.add_option("-B", "--basename", dest="basename")

(options, args) = parser.parse_args()

inputFilename=args
Mfiles=len(args)
basename="TEM"
outputFilename = basename+"__mean.DAT"

# sample file for templates

tmp_data=np.loadtxt(inputFilename[0])
drows=len(tmp_data)
dcols=len(tmp_data[0])
data_mean_std=np.zeros(drows*(dcols+1)).reshape(drows,(dcols+1)) # +1 because std
del tmp_data


# open files to read line by line
arquivo = [open(inputFilename[i]) for i in range(0,Mfiles) ]

T_i=np.zeros(Mfiles)            # array to store temperature on each position.
for k in range(0,drows):
  for m in range(Mfiles):
    line=arquivo[m].readline()
    aux=np.fromstring(line, dtype=float, sep=' ')
    pos_i=aux[0]
    T_i[m]=aux[1]
    
  data_mean_std[k] = np.array([pos_i, T_i.mean(), T_i.std()])
  
# save into a line in outFilename
np.savetxt(outputFilename, data_mean_std)

print data_mean_std
for arq in arquivo:
  arq.close()
  
print "Mfiles="+str(Mfiles)
