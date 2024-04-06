
DIR = ~/.timetracker-sway
LOG_FILE = record.csv

install: 
	if [ ! -d ${DIR} ]; then mkdir ${DIR}; fi 
	#cd src
	cp -u ./src/pre-process.py ./src/get_stats.py ./src/record_activity.sh ${DIR}
	if [ ! -f ${DIR}/categories.py ]; then cp -u ./src/sample_categories.py ${DIR}/categories.py; fi
	cd ..  
	sed -i '/alias time-stats=/d' ~/.bashrc
	echo "alias time-stats='python3 ${DIR}/get_stats.py ${DIR}/${LOG_FILE}'" >> ~/.bashrc

