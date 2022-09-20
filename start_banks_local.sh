#!/bin/bash

#Remove previous databases.
rm BANK1.db
rm BANK2.db

#Start different "Banks"
export BANK_ID="BANK1"
nohup python3 flask_api.py &> bank1_logs.rpt &
export BANK_ID="BANK2"
nohup python3 flask_api.py &> bank2_logs.rpt &
