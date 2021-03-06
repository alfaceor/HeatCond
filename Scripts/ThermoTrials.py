#!/usr/bin/python
# Script to get the time average for Temperature, Magnetization, Flux
# for each trials (realization, job) over the simulation time

import numpy as np

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
#parser.add_option("-x", "--xcolumn", dest="xcolumn")
#parser.add_option("-y", "--ycolumn", dest="ycolumn")
#parser.add_option("-X", "--Xlabel", dest="Xlabel")
#parser.add_option("-Y", "--Ylabel", dest="Ylabel")

parser.add_option("-N", "--Npart", dest="Npart")
parser.add_option("-u", "--U0", dest="U0")
parser.add_option("-A", "--alpha", dest="alpha")
parser.add_option("-t", "--transient", dest="transient")
parser.add_option("-o", "--outputFilename", dest="outputFilename")

(options, args) = parser.parse_args()

if options.Npart == None:
  Npart = 40
else:
  Npart = int(options.Npart)
  
if options.U0 == None:
  U0 = 0.10
else:
  U0 = float(options.U0)

if options.alpha == None:
  alpha = 0.50
else:
  if options.alpha == "INFT":
    # do nothing
    alpha = 100
  else:
    alpha = float(options.alpha)
  
if options.transient == None:
  transient = 200
else:
  transient = int(options.transient)
  
if options.outputFilename == None:
  outputFilename = "thermoTrial.dot"
else:
  outputFilename = options.outputFilename

def CalcNtilde(Npart, alpha):
  Ntilde=0.0
  for i in range(1,Npart+1) :
    Ntilde += i**(-alpha)
  return Ntilde

#Ntilde = CalcNtilde(Npart, alpha)

filename = args
Mfiles = len(filename)
# [ N, U0, alpha, T_mean, T_var, M_mean, M_var, J_mean, J_var] 9 vars
thermo = np.zeros(Mfiles*9).reshape(Mfiles,9)
#thermo = np.zeros(Mfiles)

for i in range(Mfiles):
  data  = np.loadtxt(filename[i])
  ttime = data[:,0]
  Ek    = data[:,1]
  Ep    = data[:,2]
  Mx    = data[:,3]
  My    = data[:,4]
  Flux  = data[:,5]
  del data
  
  T = 2*Ek[transient:]/Npart
  U0 = ((Ek[transient:] + Ep[transient:])/Npart).mean()
  M = np.sqrt(Mx**2 + My**2)[transient:]
  
  T_mean = T.mean()
  T_std  = T.std()
  
  M_mean = M.mean()
  M_std  = M.std()
  
  J_mean = Flux.mean()
  J_std  = Flux.std()
  
  thermo[i] = np.array([Npart, U0, alpha, T_mean, T_std, M_mean, M_std, J_mean, J_std])

np.savetxt(outputFilename, thermo)

# TODO: Change the values of T_var, M_var, J_var
thermoMean = thermo.mean(axis=0)

thermoMean[4]=thermo[:,3].std()
thermoMean[6]=thermo[:,5].std()
thermoMean[8]=thermo[:,7].std()

print  ' '.join(map(str, thermoMean))


