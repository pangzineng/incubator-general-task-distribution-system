#!/bin/bash

GTDS_DEFINITIONS=$(<definitions.yaml)

docker build \
    --build-arg DEFINITIONS="$GTDS_DEFINITIONS" \
    --build-arg VERSION=0.1.0 \
    --build-arg SERVER_HOST=localhost \
    --build-arg SERVER_PORT=8888 \
    --build-arg SERVRE_BASE_PATH=v1 \
    --build-arg SERVICE_NAME=AdBoardClient \
    --build-arg CUSTOM_KEY=schedule:_adboard \
    -t gtds-adboard-client:0.1.0 ../../

# run locally
docker-compose -p adboard-client down &&
docker-compose -p adboard-client up