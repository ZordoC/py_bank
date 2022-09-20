#!/bin/bash

printf "Building Docker image"
docker build -t flask-api/api:0.1.0  -f docker/Dockerfile.api .

printf "Running Bank1"
docker run --env "BANK_ID=BANK1" -p 5001:5001 -d flask-api/api:0.1.0

printf "Running Bank2"
docker run --env "BANK_ID=BANK2" -p 5002:5002 -d flask-api/api:0.1.0
