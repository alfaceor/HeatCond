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


def getData(filename):
  data=np.loadtxt(filename)
  ttime=data[:,0]
  Ek=data[:,1]
  Ep=data[:,2]
  Mx=data[:,3]
  My=data[:,4]
  del data
  return ttime, Ek, Ep, Mx, My

def Uteo(M,KT,eps):
	return KT/2.0 + (eps/2.0)*(1-M**2)

def Mteo(U,KT,eps):
	return  np.sqrt(1-2.0*(U-KT/2.0)/eps)

Nfiles = len(args)
Ek_m = np.zeros(Nfiles)
Ep_m = np.zeros(Nfiles)
Etot_m = np.zeros(Nfiles)
M_m    = np.zeros(Nfiles)
transient=200
Npart=40 #2000

fig1 = plt.figure()
fig2 = plt.figure()

ax1_1 = fig1.add_subplot(111)
ax2_1 = fig2.add_subplot(111)
data=np.loadtxt("analitic_data.dot")
Tteo=data[:,0]
#ymax=data[:,1]
Mteo=data[:,1]
Uteo=0.5*(Tteo+1-Mteo**2)

for i in range(Nfiles):  
  ttime, Ek, Ep, Mx, My = getData(args[i])
  Etot = Ek+Ep
  M    = np.sqrt(Mx**2 + My**2)
#  ax1_1.plot(ttime, Etot, label="$"+str(i)+"$")
  #ax1_1.plot(ttime,M, label="$"+str(i)+"$")
  Ek_m[i] = Ek[transient:].mean()/Npart
  Ep_m[i] = Ep[transient:].mean()/Npart
  #Etot_m[i] = Etot[transient:].mean()#/Npart
  M_m[i]    = M[transient:].mean()
  print args[i], Ek_m[i], Ep_m[i]

#plt.plot(Ek_m,Ep_m,'o-')
Temp_m = 2.0*Ek_m
U_m = Ek_m+Ep_m
print zip(U_m, Temp_m, M_m)

ax1_1.plot(U_m, Temp_m ,'o', label="$N="+str(Npart)+"$")
ax1_1.plot(Uteo,Tteo,'--', label="$Teo$")
ax1_1.grid()
ax1_1.set_xlim(-0.1,2.1)
ax1_1.set_ylim(-0.1,3.0)
ax1_1.set_xlabel("$U$")
ax1_1.set_ylabel("$T$")
ax1_1.legend(loc=4, prop={'size':20})


ax2_1.plot(U_m, M_m,'o', label="$N="+str(Npart)+"$")
ax2_1.plot(Uteo,Mteo,'--',label="$Teo$")
ax2_1.grid()
ax2_1.set_xlim(-0.1,2.1)
ax2_1.set_ylim(-0.1,1.1)
ax2_1.set_xlabel("$U$")
ax2_1.set_ylabel("$M$")
ax2_1.legend(loc=1, prop={'size':20})

fig1.tight_layout()
fig2.tight_layout()
plt.show()

#np.savetxt("",zip(Ek_m+Ep_m, 2.0*Ek_m, M_n))
#ax1_1.legend()
#T=np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2])
#ax2_1.plot(Ek_m , Etot_m, 'o-')

#plt.show()

"""
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
