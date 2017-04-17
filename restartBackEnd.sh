#!/bin/bash

# This script provide restart (for failsave) if NN classification process have more than 2Gb memory.
# I puts script in cron for start every 5 minuts and it helped me

# Kills the process, where name is 'python app.py' or 'Python app.py'
# and have there is a number starts with from 2 to 9 and have from 7 digits in a number.
# awk block gets PID of process
kill -9 $(ps -aux | grep '[p]ython app.py' | grep -E '[2-9][0-9]{6,}' | awk '{print $2}')

# Start new backend process 
cd /your_directory_with_backend/
source /path_to/python_env/bin/activate
python app.py
