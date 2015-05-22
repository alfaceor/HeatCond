#!/usr/bin/python -i
import numpy as np
import matplotlib.pyplot as plt

def gaussKT(x, KT):
  return (1/(np.sqrt(2*np.pi*KT)))*np.exp(-0.5*(x**2)/KT)


# Plot parameters
font = {'family' : 'normal',
         'weight' : 'bold',
         'size'   : 30}
plt.rc('font', **font)
plt.rc('text', usetex=True)

X = np.arange(-3,3,0.1)
KT =1.0


from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
(options, args) = parser.parse_args()

filename=args[0]

data=np.loadtxt(filename)
Naux=len(data)
print Naux
Npart=(Naux-1)/2
ttime=data[0]
vel=data[1:Naux:2]
pos=data[2:Naux:2]
del data

density, bins=np.histogram(vel, normed=True, density=True)
unity_density = density/density.sum()
widths = bins[:-1] - bins[1:]
fitKT=vel.var()
print fitKT,vel.mean()
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.bar(bins[1:], density, width=widths, alpha=0.5, color='g')

ax1.plot( X, gaussKT(X,  KT), '--', lw=2, color='r', label="$K_BT/m = "+str(KT)+"$")
ax1.plot( X, gaussKT(X,  fitKT), '.', lw=2, color='b', label="$K_BT/m = "+str(fitKT)+"$")

ax1.legend()
ax1.set_xlabel("$\omega_{i,0}$")
fig.tight_layout()



aaa=np.fmod(pos,2.0*np.pi) # FIXME: if negative must be different
bbb=np.fmod(aaa+2.0*np.pi,2.0*np.pi)
jojo=np.ones(len(bbb))

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, polar=True)
ax2.plot(bbb,jojo,'.')
fig2.tight_layout()


plt.show()
