#!/bin/bash

# requirements jq python3 python3-padas
#IFS=$'\n' 
DIR=~/.timetracker-sway

# get the PID of all the processes running
PROCESSES=$( pstree -p | grep 'record_activity' | grep -o 'record_activity([0-9]*)' | grep -o '[0-9]*' )

# get the PID of the current process
CUR_PROCESS=$$
#echo "current: $CUR_PROCESS"

# kill the other processes
for f in $PROCESSES
do
	# echo $f
	if [ $f -eq $CUR_PROCESS ] 
	then
		# echo "Current process*"
		break
	else
		kill -SIGTERM $f
	fi 
done

# run the main loop to record the information
while :
do
	NAME=$(swaymsg -t get_tree | jq '.. | (.nodes? // empty)[] | select(.focused==true).name')
	DATE=$(date +'%F')
	TIME=$(date +'%T')
	SEC=$(date +'%s')
	if [ ! -z "$NAME" ]
	then 
		readarray -t data <<< $(python3 ${DIR}/pre-process.py "$NAME" ) 
		echo "$SEC;${data[0]};${data[1]};$NAME" >> ${DIR}/record.csv
	fi
	sleep 60
done





