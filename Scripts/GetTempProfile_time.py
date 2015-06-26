#!/usr/bin/python

# TODO: Calculate the temperature profile and the system over different realization(trials).


import numpy as np
#import matplotlib.pyplot as plt

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
parser.add_option("-o", "--outfilename", dest="outfilename")
parser.add_option("-t", "--transient", dest="transient")

(options, args) = parser.parse_args()

if options.outfilename == None:
  outputFilename = "default__TempProfile.txt"
else:
  outputFilename = options.outfilename

if options.transient == None:
  transient = 200
else:
  transient = int(options.transient)


def getVel(filename):
  data=np.loadtxt(filename)
  Naux=len(data[0])
  Npart=(Naux-1)/2
  ttime=data[:,0]
  vel=data[:,1:Naux:2]
#  pos=data[:,2:Naux:2]
  del data
  return Npart, ttime, vel


Mfiles=len(args)
inputFilename=args

# I need to get the size of the system particle
Npart, ttime, vel =getVel(inputFilename[0])
particles = range(Npart)
TempVar  = vel[transient:].var(axis=0)
TempMean = (vel[transient:]**2).mean(axis=0)
TempKurt = (vel[transient:]**4).mean(axis=0)

np.savetxt(outputFilename, zip(particles,TempVar,TempMean,TempKurt))
#plt.plot(particles, TempVar , 'o-')
#plt.plot(particles, TempMean, '+-')

#plt.ylim(0.6,1.0)
#plt.ylim(0.0,3.0)
#plt.savefig(inputFilename[0]+".png")

"""
# velocity for each trial an a fixed time
vel_trial = np.zeros(Mfiles*Npart).reshape(Mfiles,Npart)
TempProf_ttime = np.zeros(len(ttime)*(Npart+1)).reshape(len(ttime),(Npart+1))
TempProf_ttime[:,0] = ttime

# open files to read
arquivo = [open(inputFilename[i]) for i in range(0,Mfiles) ]

for itime in range(len(ttime)):
  for i in range(Mfiles):
    line=arquivo[i].readline()
    aux=np.fromstring(line, dtype=float, sep=' ')
    vel_trial[i] = aux[1::2] # velocities of trial i
    #print itime, i
  
  TempProf_ttime[itime,1:]=vel_trial.var(axis=0)
  

np.savetxt(outputFilename, TempProf_ttime)
"""
