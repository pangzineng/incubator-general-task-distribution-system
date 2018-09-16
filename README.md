# server

1, Add your data model in to `swagger-spec/definitions.yaml` and the common parts to `swagger-spec/definitions_common.yaml`

2, Update your controller logic at `swagger-inject/python-flask-server/controller_template.py`

3, run script, such as: `./init.sh -v 2.1.1`, for more parameter options just read the script

4, get your latest swagger spec at `./api_swagger_specification.yaml` and your server at `./python-flask-server`


# clients

## prerequisite

- docker is installed, shared volume with host is enabled
- run below commands in the folder where `api_swagger_specification.yaml` is located

## client (python) 

`docker run --rm -v ${PWD}:/client swaggerapi/swagger-codegen-cli:v2.3.1 generate -i /client/api_swagger_specification.yaml -l python -o /client/python-client`

## client (javascript es6 with promise) 

`docker run --rm -v ${PWD}:/client swaggerapi/swagger-codegen-cli generate -i /client/api_swagger_specification.yaml -l javascript --additional-properties useEs6=true --additional-properties usePromises=true -o /client/es6-client`

Note: js client is not stable, use with care