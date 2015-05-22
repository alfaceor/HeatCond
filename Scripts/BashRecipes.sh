# bash recipes

for i in `ls *.tvr`
do 
 salida=`basename $i .tvr`.tem
 echo $salida
 GetTempProfile_time.py $i -t 2000 -o ${salida}
done


for i in `ls *[0-3]?.tvr`
do 
 salida=`basename $i .tvr`.tem
 echo $salida
 GetTempProfile_time.py $i -t 2000 -o ${salida}
done

# Create line number X into a ini file
for i in `ls *.tvr`
do
  salida=`basename $i .tvr`.ini
  sed -n 90p $i > ${salida}
done



for i in `ls *.tvr`
do 
 salida=`basename $i .tvr`.tem
 echo $salida
 GetTempProfile_time.py $i -t 2000 -o ${salida}
done


fucku=`ls T1_0.90__T2_0.70__A_[0-9]*/*0064.end`
for i in $fucku
do
 cd `dirname $i`
 for i in `ls *.tvr`
 do 
  salida=`basename $i .tvr`.tem
  echo $salida
  GetTempProfile_time.py $i -t 2000 -o ${salida}
 done
 MeanTem.py *.tem
 cd ..
done
