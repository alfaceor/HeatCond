#!/usr/bin/python 
#@alfaceor
# Energy Plot

#import matplotlib as mpl
#mpl.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
parser.add_option("-N", "--Npart", dest="Npart")
parser.add_option("-t", "--transient", dest="transient")
#parser.add_option("-p", "--numpuntos", dest="numpuntos")

(options, args) = parser.parse_args()

filename=args[0] #"N_120__T1_4__T2_4__dm_0.0__dr_1.dat"
data=np.loadtxt(filename)
ttime=data[:,0]
Ekin=data[:,1]
Epot=data[:,2]
del data

### plot

# Plot parameters
font = {'family' : 'normal',
         'weight' : 'bold',
         'size'   : 30}
plt.rc('font', **font)
plt.rc('text', usetex=True)

Npart=2000 #88
transient=10 #2000
cada=1 #10
#Figures and axes
fig = plt.figure()
fig.suptitle("$N="+str(Npart)+"$, $T_1=0.0, T_2=0.0$, $FNB$", fontsize=20)
#fig.suptitle("$N="+str(Npart)+"$, NoHB", fontsize=20)
ax1 = fig.add_subplot(111)
#ax2 = plt.axes([.25, .65, .4, .2])
#ax2 = plt.axes([.6, .25, .2, .2])


print Ekin[transient:].mean()
ax1.axvline(ttime[transient], lw=4, color='y', alpha=0.5)
ax1.axhline(Ekin[transient:].mean()/Npart, lw=1, color='b', alpha=0.7)

ax1.plot(ttime[::cada], Ekin[::cada]/Npart, label="$E_k/N$", marker='o')
ax1.plot(ttime[::cada], Epot[::cada]/Npart, label="$E_p/N$")
ax1.plot(ttime[::cada], (Ekin+Epot)[::cada]/Npart, label="$E_{tot}/N$")
#ax2.plot(ttime,Ekin)
#ax2.plot(ttime,Epot)
#ax2.plot(ttime,(Ekin+Epot))
#ax2.locator_params(axis='both',nbins=3)

#ax2.set_xlim(18,50)
#ax2.set_ylim(4.99999,5.00001)

#ax1.set_xlim(0,10**4)
#bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
#ax1.text(100000, 2, "$N=40$\n$T_1 = 1.0$",bbox=bbox_props)
#ax1.set_xlim(10**6-10**4,10**6)
#ax1.set_ylim(0,3)

ax1.set_ylabel("$E/N$")
ax1.set_xlabel("$t$")
#ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=3, mode="expand", borderaxespad=0.)
#ax1.legend(loc='upper center', bbox_to_anchor=(0.5,1.05), ncol=1, fancybox=True);
ax1.legend(loc=1,prop={'size':20})
plt.tight_layout()
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.grid()

outfilename=filename+".png"
#plt.savefig(outfilename)
plt.show()


