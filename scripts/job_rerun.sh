#!/bin/sh

# this script searches for the running task and reruns if not running. it will be scheduled by Crontab for every min.
# change python3's path if needed + the foos.py location if needed

APP_FULL_PATH="/home/pi/Projects/foos/foos.py"
PYTHON_FULL_PATH="/usr/bin/python3"

ps auxw | grep "$PYTHON_FULL_PATH $APP_FULL_PATH" | grep -v grep > /dev/null
if [ $? != 0 ]
then
       $PYTHON_FULL_PATH $APP_FULL_PATH > /dev/null
fi
