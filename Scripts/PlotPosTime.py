#!/usr/bin/python -i
#@alfaceor
# Energy Plot

#import matplotlib as mpl
#mpl.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
#parser.add_option("-k", "--kmcolumn", dest="kmcolumn")
#parser.add_option("-t", "--transient", dest="transient")
#parser.add_option("-p", "--numpuntos", dest="numpuntos")

(options, args) = parser.parse_args()

filename=args[0] #"N_120__T1_4__T2_4__dm_0.0__dr_1.trv"
data=np.loadtxt(filename)
Naux=len(data[0])
print Naux
Npart=(Naux-1)/2
ttime=data[:,0]
vel=data[:,1:Naux:2]
pos=data[:,2:Naux:2]
del data

### plot

# Plot parameters
font = {'family' : 'normal',
         'weight' : 'bold',
         'size'   : 30}
plt.rc('font', **font)
plt.rc('text', usetex=True)

#Figures and axes
fig = plt.figure()
ax1 = fig.add_subplot(111)
#ax2 = plt.axes([.6, .25, .2, .2])
zoomini=100
winsize=50
zoomend=zoomini+winsize

for i in range(Npart):
  if i<=6:
    ax1.plot(ttime,pos[:,i],label="$"+str(i)+"$")
  else:
    ax1.plot(ttime,pos[:,i],'--',label="$"+str(i)+"$")

ax1.set_xlabel("$t$")
ax1.set_ylabel("$\\theta_i$")
plt.legend(loc=2, prop={'size':14}, ncol=2)

#plt.ylim(-150, 150)
plt.ylim(-0.5*np.pi, 2.5*np.pi)
plt.grid()
plt.show()

#ax1.plot(ttime,Ekin)
#ax1.plot(ttime,Epot)
#ax1.plot(ttime,Ekin+Epot)
#ax2.plot(ttime[zoomini:zoomend],Ekin[zoomini:zoomend])
#ax2.plot(ttime[zoomini:zoomend],Epot[zoomini:zoomend])
#ax2.plot(ttime[zoomini:zoomend],(Ekin+Epot)[zoomini:zoomend])
#plt.show()


