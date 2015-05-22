#!/usr/bin/python -i
#@alfaceor
# Energy Plot

#import matplotlib as mpl
#mpl.use('Agg')
def Tk(x,T1,T2,Np):
    return (T1**(3.0/2.0)-(T1**(3.0/2.0)-T2**(3.0/2.0))*x/Np)**(2.0/3.0)

import numpy as np
import matplotlib.pyplot as plt

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 ")
#parser.add_option("-k", "--kmcolumn", dest="kmcolumn")
#parser.add_option("-t", "--transient", dest="transient")
#parser.add_option("-p", "--numpuntos", dest="numpuntos")

(options, args) = parser.parse_args()

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
#zoomini=100
#winsize=50
#zoomend=zoomini+winsize
colorArray=['b','g','r','c','m','y','k']
w=0
for filename in args:
#filename=args[0] #"N_120__T1_4__T2_4__dm_0.0__dr_1.trv"
  data=np.loadtxt(filename)
  Naux=len(data[0])
  Npart=(Naux-1)/2
  ttime=data[:,0]
  vel=data[:,1:Naux:2]
  pos=data[:,2:Naux:2]
  del data
  fluxK=vel**3
  transient=5000
  fluxK_i = fluxK[transient:].mean(axis=0)
  
  dm=0.4
  fluxK_iCorrct = np.zeros(len(fluxK_i))
  fluxK_iCorrct  = np.array([fluxK_i[i]*(1+(i%2)*dm) for i in range(Npart)])
#  Temp=vel[transient:,:].var(axis=0)
#  print Temp.var(),filename
#  etiqueta="$"+filename.split("__")[0]+"$"
#  T2=float((filename.split("__")[2]).split("_")[1])
#  etiqueta="$T_r="+str(T2)+"$"

#  TempCorrct=np.zeros(Npart)
#  dm=0.4
#  TempCorrct  = np.array([Temp[i]*(1+(i%2)*dm) for i in range(Npart)])

#  x_i=[1.0*i/Npart for i in range(Npart) ]
#  TempTeorico = np.array([Tk(x_i[i],TempCorrct[0],TempCorrct[-1],1) for i in range(Npart)])
#  ### plot

#  ax1.plot(x_i,TempCorrct ,'o-',c=colorArray[w],label=etiqueta)
#  ax1.plot(x_i,TempTeorico,'--',c=colorArray[w],label=etiqueta)
#  
#  w=w+1

#ax1.set_xlabel("$i/(N)$")
#ax1.set_ylabel("$T$")
##plt.legend()
#plt.legend(loc=8, prop={'size':20}, mode="expand", ncol=6)
#plt.ylim(0,10)
#plt.grid()
#plt.show()

##ax1.plot(ttime,Ekin)
##ax1.plot(ttime,Epot)
##ax1.plot(ttime,Ekin+Epot)
##ax2.plot(ttime[zoomini:zoomend],Ekin[zoomini:zoomend])
##ax2.plot(ttime[zoomini:zoomend],Epot[zoomini:zoomend])
##ax2.plot(ttime[zoomini:zoomend],(Ekin+Epot)[zoomini:zoomend])
##plt.show()


