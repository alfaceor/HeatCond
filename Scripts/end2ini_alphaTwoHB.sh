#!/bin/bash
set -e
U0=$1
T1=$2
T2=$3
Npart=40
Npart=`printf "%010d" ${Npart}`
basedir=/home/alfaceor/data-phd/alphaXY_TwoHB/Case001

alphaList="0.00 0.50 1.00 1.50 2.00"

for alpha in ${alphaList}
do
  cd N_${Npart}__U0_${U0}/
  cd T1_${T1}__T2_${T2}__A_${alpha}/
  mkdir -p inifiles
  mv *.ini inifiles/
  rename "s/.end/.ini/" *.end
  cd ${basedir}
done

