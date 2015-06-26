#!/bin/bash
set -e
U0=$1
T1=$2
T2=$3
Npart=40
Npart=`printf "%010d" ${Npart}`
basedir=/home/alfaceor/data-phd/alphaXY_TwoHB/Case001

alphaList="0.00 0.50 1.00 1.50 2.00"
#U0List="0.10 0.30 0.50 0.70 0.90 1.10 1.30 1.50"

scriptsPath=/home/alfaceor/Projects/HeatCond/Scripts

for alpha in ${alphaList}
do
  workdir=N_${Npart}__U0_${U0}/T1_${T1}__T2_${T2}__A_${alpha}
  echo ${workdir}
  cd ${workdir}
  for i in `ls *.tvr`
  do
    salida=`basename $i .tvr`.tem
    echo $salida
    ${scriptsPath}/GetTempProfile_time.py $i -t 1000 -o ${salida}
  done
  ${scriptsPath}/MeanTem.py *.tem
  echo ${PWD}
  cd ${basedir}
done
