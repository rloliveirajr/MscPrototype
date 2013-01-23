#!/bin/bash
dir=$(pwd)
if [ $# -eq 0 ]; then
  echo ""
  echo "Classifier Index:"
  echo ' - CLASSIFIER_ISMAEL = 1'
  echo " - CLASSIFIER_ROBERTO = 2"
  echo " - CLASSIFIER_CWA = 3"
  echo " - CLASSIFIER_RANDOM_CWA = 4"
  echo " - CLASSIFIER_CWA_2_WAY= 5"
  echo "============================="
  echo "Exceute classifier: ./run.sh <index_of_classifier> <num_repetitions>"
  echo ""
else
  i=$1
  max=$2
  for rr in `seq 1 $max`
  do
    echo $rr  
    for f in $(ls $dir/dataset)
    do
      echo $d/dataset/$f
      echo "$dir/src/main.py -d $f -f $dir/dataset/$f -r $dir/resource/ -t $dir/temp_dir/ -o $dir/results/ "
      python $dir/src/main.py -c $i -d $f -f $dir/dataset/$f -r $dir/resource/ -t $dir/temp_dir/ -o $dir/results/ >> tmp
    done
   done
fi
