#!/bin/sh

# this script searches for the running task and reruns if not running. it will be scheduled by Crontab for every min.
# change python3's path if needed + the foos.py location if needed

BASE_PATH="/home/pi/Documents/workspaces/foos"
APP_FULL_PATH="$BASE_PATH/foos.py"
VENV_PATH="$BASE_PATH/venv/bin"

ps auxw | grep "python3 ./foos.py" | grep -v grep > /dev/null
if [ $? != 0 ]
then
       source $VENV_PATH/activate
       cd $BASE_PATH
       python3 ./foos.py > /dev/null &
fi
