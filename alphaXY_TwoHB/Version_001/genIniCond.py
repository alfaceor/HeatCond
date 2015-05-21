#!/usr/bin/python

# TODO: Create a script to generate the initial conditions of a system with N particles and a Etot as parameters.

import numpy as np

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
parser.add_option("-N", "--Npart", dest="Npart")
parser.add_option("-u", "--U0", dest="U0")
parser.add_option("-j", "--job_id", dest="job_id")
parser.add_option("-1", "--T1", dest="T1")
parser.add_option("-2", "--T2", dest="T2")
parser.add_option("-A", "--alpha", dest="alpha")


(options, args) = parser.parse_args()

# water-bag conditions
#vel = np.zeros(Npart)
#Nmid=Npart/2
#for i in range(Nmid):
#  vel[i]  = np.random.uniform()
#  vel[i+Nmid] = -vel[i]

if options.Npart == None:
  Npart = 500
else:
  Npart = int(options.Npart)
strNpart = str(Npart).zfill(10)
  
if options.U0 == None:
  U0 = 1.00
  options.U0='1.00'
else:
  U0 = float(options.U0)
strU0=options.U0

if options.job_id ==None:
  strJob_id = "00000"
else:
  strJob_id = (options.job_id).zfill(5)

if options.T1 ==None:
  T1=0.00
  options.T1='0.00'
else:
  T1  = float(options.T1)
strT1=options.T1

if options.T2 ==None:
  T2=0.00
  options.T2='0.00'
else:
  T2  = float(options.T2)
strT2=options.T2

if options.alpha ==None:
  alpha =0.00
  options.alpha='0.00'
else:
  alpha = float(options.alpha)
strAlpha=options.alpha


# FIXME: make this name composition more beatifull
#filename="N_"+str(Npart).zfill(10)+"__U0_"+options.U0+"__T1_"+options.T1+"__T2_"+options.T2+"__id_"+job_id+".ini"
filename="N_"+strNpart+"__U0_"+strU0+"__T1_"+strT1+"__T2_"+strT2+"__A_"+strAlpha+"__id_"+strJob_id+".ini"

time = 0.0 # Could be any number just to get the same format!.

# Gaussian initial conditions
vel = np.zeros(Npart)
vel = np.random.normal(0.0, 1.0, Npart)
vel = vel - vel.mean()
vel = vel/np.sqrt(vel.var())
vel = np.sqrt(2.0*U0)*vel

# All the angles initiate with zero (Epot=0.0).
pos = np.zeros(Npart)
vec_m = np.array([[np.cos(pos[i]),np.sin(pos[i])] for i in range(Npart)])

vec_M = vec_m.mean(axis=0)
Ekin = 0.5*vel.var() # m=1.0
Epot = 0.5*(1- vec_M[0]*vec_M[0] - vec_M[1]*vec_M[1] )

U = Ekin+Epot
print Ekin, Epot, U
ini = np.empty((1+vel.size + pos.size,), dtype=vel.dtype)
ini[0] = 0.0
ini[1::2] = vel
ini[2::2] = pos
#print ini[None]

# i need a way to generate an initial total energy in the system
np.savetxt(filename,ini[None],fmt='%.6e')
print filename











###### DRAFT ##########
#with open(filename,'wb') as f:
#  f.write(b''+headerfile)
#  np.savetxt(f,zip(yk,D[:,0],D[:,1],D[:,2],D[:,3]))
#  f.close()

