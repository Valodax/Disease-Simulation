#!/bin/bash

exp_dir=Simulation_Parameter_Sweep_`date "+%Y-%m-%d_%H:%M:%S"`
exp_dir2=trial_stats

mkdir $exp_dir
cp diseaseSim.py $exp_dir
cp params.sh $exp_dir
cp barriers.csv $exp_dir
cd $exp_dir
mkdir $exp_dir2

n=$1
pop=$2
infect=$3
immune=$4
steps=$5
low_i=$6
high_i=$7
step_i=$8
low_r=$9
high_r=${10}
step_r=${11}
low_d=${12}
high_d=${13}
step_d=${14}

echo "### PARAMETERS: ###"
echo "Neighbourhood type: "$n
echo "Total Population: " $pop
echo "Number of people starting as infected: " $infect
echo "Number of people starting as immune: " $immune
echo "Probability of Infection: " $low_i $high_i $step_i
echo "Probability of Recovery: " $low_r $high_r $step_r
echo "Probability of Death: " $low_d $high_d $step_d
echo "Number of Steps: " $steps

for i in `seq $low_i $step_i $high_i`;
do
	for j in `seq $low_r $step_r $high_r`;
	do
		for k in `seq $low_d $step_d $high_d`;
		do
			c=$((c+1))
			echo "Experiment: "$c $n $pop $infect $immune $steps $i $j $k
			outfile="diseaseSim_Trial_"$c".txt"
			python3 diseaseSim.py $n $pop $infect $immune $steps $i $j $k $c > $outfile
			mv $outfile $exp_dir2

		done
	done
done

