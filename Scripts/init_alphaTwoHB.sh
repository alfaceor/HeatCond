#!/bin/bash
set -e
basedir=/home/alfaceor/data-phd/alphaXY_TwoHB/Case001
exec_path=/home/alfaceor/Projects/HeatCond/alphaXY_TwoHB/Version_002
#exec_path=/home/alfaceor/Projects/ceor-phd/alphaXY_TwoHB/Version_001
main_prog=mainAlphaTwoHB001

N=40
N=`printf "%010d" ${N}`
U0=$1
T1=$2
T2=$3
alpha=2.00  #$1 #1.30
id_from=1
id_to=100

cd ${basedir}
SUBDIR01=N_${N}__U0_${U0}
SUBDIR02=T1_${T1}__T2_${T2}__A_${alpha}

mkdir -p ${SUBDIR01}
mkdir -p ${SUBDIR01}/${SUBDIR02}

#INIFILE=N_${N}__U0_${U0}__T1_${T1}__T2_${T2}__id_${job_id}.ini

cd ${SUBDIR01}/${SUBDIR02}

# Do not overwrite files
if ls *.end 1> /dev/null 2>&1;
then
 echo "Warning the end files already exists!"
else
 ## TODO: check if directory and end files exist
 #cp ../T1_0.00__T2_0.00__A_${alpha}/*.end .
 #rename "s/.end/.ini/" *.end
 #rename "s/T1_0.00__T2_0.00/T1_${T1}__T2_${T2}/" *.ini
 echo "Rerun from end to ini"
fi


## Create InputParams.prm
PARAMSFILE=InputParams.prm
cat > ${PARAMSFILE} <<- EndOfMessage
Npart=${N}
U0=${U0}
T1=${T1}
T2=${T2}
alpha=${alpha}
eps=1.0
gamma1=1.0
gamma2=1.0
total_time=1000000
timeDim=10000
dt=0.001
EndOfMessage

## Create file to submit (torque)
qsubfile=submit_job.q
cat > ${qsubfile} <<- EndOfMessage
#!/bin/sh
#PBS -d ${basedir}/${SUBDIR01}/${SUBDIR02}

#PBS -l walltime=24:00:00
#PBS -m e
#PBS -M alfaceor@gmail.com

date
#/home/alfaceor/Projects/ceor-phd/alphaXY_TwoHB/Version_001
exec_path=${exec_path}
#mainAlphaTwoHB001
main_prog=${main_prog}

N=${N}
U0=${U0}
T1=${T1}
T2=${T2}
alpha=${alpha}
EndOfMessage

cat ${basedir}/qsubTemplate.sh >> ${qsubfile}

## Just print job
echo qsub -t ${id_from}-${id_to} ${qsubfile}

# read -r -p "Do you want to run in the cluster? [y/N] " response
# if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
# then
    qsub -N ${U0}_${alpha} -t ${id_from}-${id_to} ${qsubfile}
# else
#     echo "Ok maybe the next time"
# fi

## Calculate temperature profile



## Calculate means magnetization, flux
