#!/bin/bash

GTDS_DEFINITIONS=$(<definitions.yaml)

docker build \
    --build-arg DEFINITIONS="$GTDS_DEFINITIONS" \
    --build-arg VERSION=0.1.0 \
    --build-arg SERVER_HOST=localhost \
    --build-arg SERVER_PORT=8888 \
    --build-arg SERVRE_BASE_PATH=v1 \
    --build-arg SERVICE_NAME=AdBoardClientScheduler \
    --build-arg CUSTOM_KEY=schedule:adboard._id \
    -t gtds-adboard-client-scheduler:0.1.0 ../../

# run locally
docker-compose -p adboard-client-scheduler down &&
docker-compose -p adboard-client-scheduler up