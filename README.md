# Introduction

It's a simple web server wrapped around the output of [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) for python flask server.

It's the server part of the 3 part general data management system
- **ui**: https://github.com/pangzineng/incubator-general-operation-ui
- **gateway**: https://github.com/pangzineng/incubator-general-system-gateway
- **server**: https://github.com/pangzineng/incubator-general-task-distribution-system

# Setup

Follow any one of the [example](./example) (no need to care about the actual data schema) starting at `run.sh` to see how the docker image was built with the pre-defined data schema (in [Swagger 2.0 syntax](https://swagger.io/docs/specification/2-0/basic-structure/))

Below is a template for the build, only `DEFINITIONS` argument is mandatory, which is the stringified data schema
```bash
docker build \
    --build-arg DEFINITIONS="$DEFINITIONS" \
    --build-arg VERSION="$VERSION" \
    --build-arg SERVER_HOST="$SERVER_HOST" \
    --build-arg SERVER_PORT="$SERVER_PORT" \
    --build-arg SERVRE_BASE_PATH="$SERVRE_BASE_PATH" \
    --build-arg SERVICE_NAME="$SERVICE_NAME" \
    -t ${IMAGE_NAME}:${IMAGE_TAG} .
```