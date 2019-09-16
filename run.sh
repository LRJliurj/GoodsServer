#/bin/bash
runId=`ps -ef | grep python3 | grep -w 8000 | awk 'BEGIN{FS=" "}{print $2}'`
kill -9 $runId
source activate goodserver
nohup python3 manage.py runserver 127.0.0.1:8000 &
source deactivate goodserver
