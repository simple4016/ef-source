#!/bin/bash

HOST=$1
PROJECT_ID=$2

while true
do
  python3 timer.py --host $HOST --project_id $PROJECT_ID
  TIME_NOW=$(date +"%Y/%m/%d %H:%M:%S")
  echo "$TIME_NOW restart timer..."
  sleep 1
done
