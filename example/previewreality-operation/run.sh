#!/bin/bash

GTDS_DEFINITIONS=$(<definitions.yaml)

docker build \
    --build-arg DEFINITIONS="$GTDS_DEFINITIONS" \
    --build-arg VERSION=0.1.0 \
    --build-arg SERVER_HOST=localhost \
    --build-arg SERVER_PORT=8888 \
    --build-arg SERVRE_BASE_PATH=v1 \
    --build-arg SERVICE_NAME=PreviewReality \
    -t gtds-previewreality-operation:0.1.0 ../../

# run locally
docker-compose -p previewreality-operation down &&
docker-compose -p previewreality-operation up