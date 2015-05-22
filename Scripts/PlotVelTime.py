#!/usr/bin/python -i
#@alfaceor
# Energy Plot

#import matplotlib as mpl
#mpl.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

# Plot parameters
font = {'family' : 'normal',
         'weight' : 'bold',
         'size'   : 30}
plt.rc('font', **font)
plt.rc('text', usetex=True)


from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
#parser.add_option("-k", "--kmcolumn", dest="kmcolumn")
#parser.add_option("-t", "--transient", dest="transient")
#parser.add_option("-p", "--numpuntos", dest="numpuntos")

(options, args) = parser.parse_args()

Mfiles=len(args)
inputFilename=args

#Figures and axes
fig1 = plt.figure()
#fig2 = plt.figure()
ax1_1 = fig1.add_subplot(111)
#ax2_1 = fig2.add_subplot(111)
#ax2 = plt.axes([.6, .25, .2, .2])

for m in range(Mfiles):
  data=np.loadtxt(inputFilename[m])
  Naux=len(data[0])
  Npart=(Naux-1)/2
  ttime=data[:,0]
  vel=data[:,1:Naux:2]
  pos=data[:,2:Naux:2]
  del data

  particle_id = [0, 19]#, 1, 2, 3] #, 1, 20, 38, Npart-1]#range(Npart)
  for i in particle_id:
    ax1_1.plot(ttime,vel[:,i],label="$"+str(i)+", "+str(m)+"$")
#    if i<=6:
#      ax1.plot(ttime,vel[:,i],label="$"+str(i)+"$")
#    else:
#      ax1.plot(ttime,vel[:,i],'--',label="$"+str(i)+"$")

  ax1_1.set_xlabel("$t$")
  ax1_1.set_ylabel("$\\omega_i$")
#  ax2_1.set_xlabel("$t$")
#  ax2_1.set_ylabel("$\\theta_i$")
#  ax1_1.set_ylim(-0.5*np.pi, 2.5*np.pi)
  plt.legend(loc='best', prop={'size':14})
  plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
  plt.tight_layout()
#plt.xlim(0, 150)

plt.grid()
plt.show()


