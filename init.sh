#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
SWAGGER=api_swagger_specification.yaml

while getopts ":v:o:n:d:" opt; do
  case $opt in
    v) 
      arg_v="$OPTARG"
      ;;
    o) 
      arg_o="$OPTARG"
      ;;
    n) 
      arg_n="$OPTARG"
      ;;
    d) 
      arg_d="$OPTARG"
      ;;
  esac
done

VERSION=${arg_v:-0.0.1}
OUTPUT_DIR=${arg_o:-${SCRIPT_DIR}}
SERVER_NAME=${arg_n:-python-flask-server}
DOCK_REGISTRY=${arg_d:-pangzineng}

## prepare swagger generator

docker build -t swagger-generator swagger-generator

docker run --rm -v ${SCRIPT_DIR}/swagger-spec:/input swagger-generator ${VERSION} > ${OUTPUT_DIR}/${SWAGGER}

## server generation (python flask)

### generate server shell with swagger-codegen
docker run --rm -v ${OUTPUT_DIR}:/server pangzineng/swagger-codegen-cli:v2.3.1 generate -i /server/${SWAGGER} -l python-flask -o /server/${SERVER_NAME}
### change the ownership of shell (because docker always write as root)
sudo chown $(id -u -n):$(id -g -n) -R ${OUTPUT_DIR}/${SERVER_NAME}
### inject controller logic into server shell
python ${SCRIPT_DIR}/swagger-inject/${SERVER_NAME}/run.py -p ${OUTPUT_DIR}/${SERVER_NAME}

## server image build & push

docker build -t $DOCK_REGISTRY/${SERVER_NAME}:$VERSION ${OUTPUT_DIR}/${SERVER_NAME} &&
echo "Local process finish, to upload"
docker push $DOCK_REGISTRY/${SERVER_NAME}:$VERSION

## clean up
rm -rf ${OUTPUT_DIR}/${SERVER_NAME}
