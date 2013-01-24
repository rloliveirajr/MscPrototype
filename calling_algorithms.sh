#!/bin/bash
dataset_path=$1
dataset=$2
resource=$3
result=$4
tmp=$5
nclasses=$6
size_random=$7
window_size=$8
seed=$9

# echo "Algoritmo SIGIR2011"
# python ./src/main.py -c 7 -f $dataset_path -o $result -d $dataset --resource $resource --nclasses $nclasses --rules_size 3 --tmp_dir $tmp --seed $seed --confidence 0.01 --support 0.01 --min_confidence 0.7 --max_timestamp 5 > /dev/null

# echo "Algoritmo SBBD 2011"
# python ./src/main.py -c 6 -f $dataset_path -o $result -d $dataset --resource $resource --nclasses $nclasses --rules_size 3 --tmp_dir $tmp --seed $seed --confidence 0.01 --support 0.01 --is_fixed False --score_max 0.01 --window_size $window_size > /dev/null
# 
# echo "Algoritmo LAC Sliding Window"
# python ./src/main.py -c 6 -f $dataset_path -o $result -d $dataset --resource $resource --nclasses $nclasses --rules_size 3 --tmp_dir $tmp --seed $seed --confidence 0.01 --support 0.01 --is_fixed True --score_max 0.01 --window_size $window_size > /dev/null

# echo "Algoritmo Extended Lac-Wcpc"
# python ./src/main.py -c 5 -f $dataset_path -o $result -d $dataset --resource $resource --nclasses $nclasses --rules_size 3 --tmp_dir $tmp --seed $seed > /dev/null
# 
# echo "Algoritmo Lac-Wcpc"
# python ./src/main.py -c 3 -f $dataset_path -o $result -d $dataset --resource $resource --nclasses $nclasses --rules_size 3 --tmp_dir $tmp --seed $seed > /dev/null
# 
# echo "Algoritmo Lac-WpcRw: Random"
# for i in $(seq 10) 
# do 
#echo "($i) Algoritmo Lac-WpcRw: Random"
# python ./src/main.py -c 4 -f $dataset_path -o $result -d $dataset --resource $resource --nclasses $nclasses --rules_size 3 --tmp_dir $tmp --seed $seed --is_random True --size_random -1 > /dev/null
# done

echo "Algoritmo Lac-WpcRw: Fixed - Size Random: $size_random"
for i in $(seq 10)
do 
echo "($i) Algoritmo Lac-WpcRw: Fixed - Size Random: $size_random"
python ./src/main.py -c 4 -f $dataset_path -o $result -d $dataset --resource $resource --nclasses $nclasses --rules_size 3 --tmp_dir $tmp --seed $seed --is_random False --size_random $size_random > /dev/null
done
# 
# echo "Algoritmo Lac-Wpc"
# python ./src/main.py -c 2 -f $dataset_path -o $result -d $dataset --resource $resource --nclasses $nclasses --rules_size 3 --tmp_dir $tmp --seed $seed > /dev/null
# 
# echo "Algoritmo Lac-Incremental"
# python ./src/main.py -c 1 -f $dataset_path -o $result -d $dataset --resource $resource --nclasses $nclasses --rules_size 3 --confidence 0.01 --support 0.01 --tmp_dir $tmp --seed $seed > /dev/null
