#!/usr/bin/python

import numpy as np

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
parser.add_option("-M", "--Mfiles", dest="Mfiles")
#parser.add_option("-B", "--basename", dest="basename")

(options, args) = parser.parse_args()

#Mfiles=30
#Read file line by line
#basename= args[0] #"N_0000002000__U0_0.69"
#inputBasename = basename+"/"+basename
#inputFilename = [inputBasename+"__id_"+str(i).zfill(5)+".dat" for i in range(1,Mfiles+1)]

inputFilename=args
Mfiles=len(args)
basename="TEM"

data_mean=np.loadtxt(inputFilename[0])

outputFilename = basename+"__mean.dat"
# open files to read line by line
arquivo = [open(inputFilename[i]) for i in range(0,Mfiles) ]
for i in range(Mfiles):
  line=arquivo[i].readline()
  aaa=np.fromstring(line, dtype=float, sep=' ')
  
data_mean[0]=aaa

data_trial = np.zeros(Mfiles*len(aaa)).reshape(Mfiles,len(aaa))
for k in range(1,len(data_mean)):
  for i in range(Mfiles):
    line=arquivo[i].readline()
    data_trial[i]=np.fromstring(line, dtype=float, sep=' ')
    # To calculate the mean of M = \sqrt{M_x^2 + M_y^2}
    # for each trial i must calculate
#    data_trial[i][3]=np.sqrt(data_trial[Mfiles-1][3]**2 + data_trial[Mfiles-1][4]**2)
#    data_trial[i][4]=0.0
#    print i, line
#  print "--"+str(k)+"--"
  data_mean[k] =  data_trial.mean(axis=0)
# save into a line in outFilename
np.savetxt(outputFilename, data_mean)

print data_mean
for arq in arquivo:
  arq.close()
  
print "Mfiles="+str(Mfiles)
