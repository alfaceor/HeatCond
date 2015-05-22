#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import os

##################

from optparse import OptionParser
parser = OptionParser("usage:  %prog [options] arg1 arg2")
parser.add_option("-o", "--outfile", dest="outfilename",
                  help="--outfile <FILENAME.png>", metavar="FILE")
parser.add_option("-x", "--xcol", dest="xcol")
parser.add_option("-y", "--ycol", dest="ycol")
parser.add_option("-s", "--subtitle", dest="subtitle")
parser.add_option("-l", "--labels", dest="col_labels")
parser.add_option("-e", "--every", dest="every")

(options, args) = parser.parse_args()

# Input filename
inputfilename=args[0]

firstline = open(inputfilename).readline()
if firstline[0] == '#':
  col_labels = firstline[1:].split()
else :
  col_labels=['tau', 'Correlation', 'KincEnerg','PotentEnerg', 'Rg', 'Z', 'HRg','PRg']

# Columns to compare
if options.xcol == None :
  xcol=1
else:
  xcol=int(options.xcol)
  
if options.ycol == None :
  ycol=2
else:
  ycol=int(options.ycol)

# Output filename
out_exten=".pdf"
if options.outfilename == None :
  outputfilename=str(inputfilename)[:-4]+"_"+col_labels[ycol-1]+"-"+col_labels[xcol-1]+out_exten
else:
  # FIXME: Validate different name of the input to avoid overwrite
  outputfilename= str(options.outfilename)

# Example data
data = np.loadtxt(inputfilename)
theox = np.sin(np.arange(0,10, 0.02))
theoy = np.cos(np.arange(0,10, 0.02))

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 24}
plt.rc('font', **font)
plt.rc('text', usetex=True)

#plt.rc('font', family='serif')
#print data[:,xcol], data[:,ycol]

plt.plot(data[:,xcol], data[:,ycol],linestyle='_', marker='o',markevery=5000,alpha=0.5, color='blue')

plt.plot(theox, theoy, label=r'$x^2+v^2$')

data = np.loadtxt(args[1])
plt.plot(data[:,xcol], data[:,ycol],linestyle='_', marker='x',markevery=5000,alpha=1.0, color='red')

plt.xlim(0.95,1.05)
plt.ylim(-0.5,0.5)
plt.xlabel(r'$x$',fontsize=24)
plt.ylabel(r'$v$',fontsize=24)
plt.grid()
#plt.legend()

plt.savefig(outputfilename,transparent=True)
plt.show()
