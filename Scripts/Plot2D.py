#!/usr/bin/python
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
parser.add_option("-x", "--xcolumn", dest="xcolumn")
parser.add_option("-y", "--ycolumn", dest="ycolumn")
parser.add_option("-X", "--Xlabel", dest="Xlabel")
parser.add_option("-Y", "--Ylabel", dest="Ylabel")

(options, args) = parser.parse_args()

if options.xcolumn == None:
  xcolumn = 0
else:
  xcolumn = int(options.xcolumn)
  
if options.ycolumn == None:
  ycolumn = 1
else:
  ycolumn = int(options.ycolumn)

if options.Xlabel == None:
  Xlabel ="$"+str(xcolumn)+"$"
else:
  Xlabel = "$"+options.Xlabel+"$"
  
if options.Ylabel == None:
  Ylabel ="$"+str(ycolumn)+"$"
else:
  Ylabel = "$"+options.Ylabel+"$"


fig1 = plt.figure()
ax1_1 = fig1.add_subplot(111)

Mfiles=len(args)
inputFilename=args
#etiqueta=["$NoHB$", "$T_1=1.0, T_2=1.0$", "$T_1=1.0, T_2=2.0$", "$T_1=2.0, T_2=2.0$"]
#etiqueta=["$\\alpha=0.0$", "$\\alpha=0.5$", "$\\alpha=1.0$", "$\\alpha=1.5$", "$\\alpha=\\infty$"]

etiqueta=[
"$\\alpha=1.00$",
"$\\alpha=1.10$",
#"$\\alpha=1.20$",
#"$\\alpha=1.30$",
"$\\alpha=1.50$",
"$\\alpha=2.00$",
#"$\\alpha=2.50$",
"$\\alpha=3.00$",
"$\\alpha=5.00$",
"$\\alpha=9.00$",
#"$\\alpha=0.10$",
#"$\\alpha=0.20$",
#"$\\alpha=0.30$",
#"$\\alpha=0.40$",
#"$\\alpha=0.50$",
#"$\\alpha=0.60$",
#"$\\alpha=0.75$",
#"$\\alpha=0.80$",
#"$\\alpha=1.00$",
#"$\\alpha=1.10$",
#"$\\alpha=1.20$",
#"$\\alpha=1.30$",
#"$\\alpha=1.50$",
#"$\\alpha=2.00$",
#"$\\alpha=2.50$",
#"$\\alpha=3.00$",
#"$\\alpha=5.00$",
#"$\\alpha=9.00$"
"line"
]



#etiqueta=[
#"$i=10, J_i = 0.007025, \\kappa = 1.4050$",
#"$i=15, J_i = 0.006122, \\kappa = 1.2245$",
#"$i=20, J_i = 0.005769, \\kappa = 1.1538$",
#"$i=25, J_i = 0.005760, \\kappa = 1.1520$",
#"$i=30, J_i = 0.005296, \\kappa = 1.0593$",
#"$i=35, J_i = 0.005678, \\kappa = 1.1357$"
#]
simbolo =["o-", "+-", "*-",".-", ">-","<-", "1-", "s-", "^-", "--"]
for m in range(Mfiles):
  data=np.loadtxt(inputFilename[m])
  X=data[:,xcolumn]
  Y=data[:,ycolumn]
  #ax1_1.plot(X,Y, simbolo[m%4], label=etiqueta[m], linewidth=2)
  ax1_1.plot(X,Y)
  


ax1_1.set_xlabel(Xlabel)
ax1_1.set_ylabel(Ylabel)
#ax1_1.set_ylim(0,2)
plt.legend(loc='best', prop={'size':14})
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.tight_layout()
plt.show()
