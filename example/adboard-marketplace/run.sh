#!/bin/bash

GTDS_DEFINITIONS=$(<definitions.yaml)

docker build \
    --build-arg DEFINITIONS="$GTDS_DEFINITIONS" \
    --build-arg VERSION=0.1.0 \
    --build-arg SERVER_HOST=localhost \
    --build-arg SERVER_PORT=8888 \
    --build-arg SERVRE_BASE_PATH=v1 \
    --build-arg SERVICE_NAME=Marketplace \
    --build-arg CUSTOM_KEY=adslot:_adboard \
    -t gtds-adboard-marketplace:0.1.0 ../../

# run locally
docker-compose -p gtds-adboard-marketplace down &&
docker-compose -p gtds-adboard-marketplace up