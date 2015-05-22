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

filename=args[0] #"N_120__T1_4__T2_4__dm_0.0__dr_1.dat"
data=np.loadtxt(filename)
ttime=data[:,0]
Mx=data[:,3]
My=data[:,4]
del data

### plot

# Plot parameters
font = {'family' : 'normal',
         'weight' : 'bold',
         'size'   : 30}
plt.rc('font', **font)
plt.rc('text', usetex=True)

#Figures and axes
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
#ax2 = plt.axes([.25, .65, .4, .2])
#ax2 = plt.axes([.6, .25, .2, .2])
zoomini=0#5000
winsize=100000
zoomend=zoomini+winsize

M   = np.sqrt(Mx**2 + My**2)
phi = np.arctan(Mx/My)

ax1.plot(ttime,Mx, label="$M_x$")
ax1.plot(ttime,My, label="$M_y$")
ax1.plot(ttime,M, label="$M$")
ax1.set_xlabel("$t$")
ax1.legend(loc=4, prop={'size':20})


fig2 = plt.figure()

ax1f2 = fig2.add_subplot(111)
ax1f2.plot(ttime,phi,'+-')
#ax1f2.set_ylim(-2,1)
ax1f2.set_xlabel("$t$")
ax1f2.set_ylabel("$\\phi$")


fig3 = plt.figure()
ax = fig3.add_subplot(111, polar=True)

colors = phi
area= 100*M**2
#ax.plot(phi, M,'o')
#c = plt.scatter(phi, M, c=colors, s=area, cmap=plt.cm.hsv)
c = ax.scatter(phi, M, c=colors, s=area, cmap=plt.cm.hsv)
ax.set_rmax(1.2)
c.set_alpha(0.75)




fig4 = plt.figure()
transient=0
ax4 = fig4.add_subplot(111, aspect='equal')
ax4.plot(Mx[transient:],My[transient:],'o-', alpha=0.7, mfc='orange')
ax4.set_xlabel("$M_x$")
ax4.set_ylabel("$M_y$")
plt.grid()

fig5 = plt.figure()
ax5 = fig5.add_subplot(111)
ax5.hist(M, normed=True, alpha=0.5, bins=25)
ax5.hist(Mx, normed=True, alpha=0.5, bins=25)
ax5.hist(My, normed=True, alpha=0.5, bins=25)
ax5.set_xlabel("$M$")
plt.show()


"""
ax1.plot(ttime,Ekin, label="$E_k$")
ax1.plot(ttime,Epot, label="$E_p$")
ax1.plot(ttime,Ekin+Epot, label="$E_{tot}$")
ax2.plot(ttime[zoomini:zoomend],Ekin[zoomini:zoomend])
ax2.plot(ttime[zoomini:zoomend],Epot[zoomini:zoomend])
ax2.plot(ttime[zoomini:zoomend],(Ekin+Epot)[zoomini:zoomend])
#ax2.locator_params(axis='both',nbins=3)

ax2.set_xlim(18,50)
ax2.set_ylim(4.99999,5.00001)

ax1.set_ylim(0,10)

ax1.set_ylabel("$E$")
ax1.set_xlabel("$t$")
ax1.legend();
plt.tight_layout()
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.show()
"""

