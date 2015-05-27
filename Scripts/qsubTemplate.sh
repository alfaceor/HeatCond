
#N=`printf "%010d" ${N}`
job_id=`printf "%05d" ${PBS_ARRAYID}`

echo `hostname`
echo ${N}
echo ${job_id}

PARAMSFILE="InputParams.prm"
if [ -f ${PARAMSFILE} ];
then
  echo "File ${PARAMSFILE} exists."
  
  INIFILE=N_${N}__U0_${U0}__T1_${T1}__T2_${T2}__A_${alpha}__id_${job_id}.ini
  if [ -f ${INIFILE} ];
  then
    date
    echo "File ${INIFILE} exists."
    ${exec_path}/${main_prog} -N ${N} -u ${U0} -1 ${T1} -2 ${T2} -A ${alpha} -j ${job_id}
  else
    echo "File ${INIFILE} does not exist."
  fi
else
   echo "File ${PARAMSFILE} does not exist."
fi

date

echo "PBS SCRIPT END"
