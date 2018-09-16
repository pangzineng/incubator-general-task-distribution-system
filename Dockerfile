FROM python:3.6 AS py3

# environment variable
ARG DEFINITIONS
ARG VERSION
ARG SERVER_SPEC_FILE
ARG SERVER_HOST
ARG SERVER_PORT
ARG SERVRE_BASE_PATH
ARG SERVER_NAME

ENV DEFINITIONS ${DEFINITIONS}
ENV VERSION ${VERSION:-0.0.1}
ENV SERVER_SPEC_FILE=${SERVER_SPEC_FILE:-api_swagger_specification.yaml}
ENV SERVER_HOST=${SERVER_HOST:-localhost}
ENV SERVER_PORT=${SERVER_PORT:-8888}
ENV SERVRE_BASE_PATH=${SERVRE_BASE_PATH:-v1}
ENV SERVER_NAME=${SERVER_NAME:-python-flask-server}

## load codes into image
COPY requirements.txt .
RUN pip3 install -r requirements.txt
## generate spec
COPY etc/spec etc/spec
COPY bin/spec-generation.py bin/spec-generation.py
RUN python bin/spec-generation.py ${VERSION} --host ${SERVER_HOST}:${SERVER_PORT} --basepath ${SERVRE_BASE_PATH} --definitions "${DEFINITIONS}" --output ${SERVER_SPEC_FILE}

## generate server
FROM openjdk:8 AS j8
ENV SERVER_SPEC_FILE=${SERVER_SPEC_FILE:-api_swagger_specification.yaml}
ENV SERVER_NAME=${SERVER_NAME:-python-flask-server}
COPY bin/swagger-codegen-cli-2.3.1.jar bin/swagger-codegen-cli-2.3.1.jar
COPY --from=py3 /etc/${SERVER_SPEC_FILE} /etc/${SERVER_SPEC_FILE}
RUN mkdir -p /server \
  &&  java -jar bin/swagger-codegen-cli-2.3.1.jar generate -i /etc/${SERVER_SPEC_FILE} -l python-flask -o /server/${SERVER_NAME} 

## build the server and run
FROM python:3-alpine
ENV SERVER_NAME=${SERVER_NAME:-python-flask-server}
ENV SERVER_PORT=${SERVER_PORT:-8888}
ARG WORKER_NUMBER
ENV WORKER_NUMBER=${WORKER_NUMBER:-4}
COPY bin/code-injection.py /bin/code-injection.py
COPY etc/python-flask-server /etc/python-flask-server 
COPY --from=j8 /server/${SERVER_NAME} /server/${SERVER_NAME}
RUN python /bin/code-injection.py --path /server/${SERVER_NAME} --temdir /etc/python-flask-server --port ${SERVER_PORT}
RUN apk --update add --virtual build-dependencies build-base \
  && pip install --no-cache-dir -r /server/${SERVER_NAME}/requirements.txt \
  && apk del build-dependencies
WORKDIR /server/${SERVER_NAME}
CMD gunicorn --workers=${WORKER_NUMBER} --bind 0.0.0.0:${SERVER_PORT} swagger_server.__main__:app

## environment variable for run time (specified via running)
# ENV RABBITMQ_DEFAULT_USER
# ENV RABBITMQ_DEFAULT_PASS
# ENV RABBITMQ_HOST
# ENV RABBITMQ_PORT
# ENV MONGODB_HOST
# ENV MONGODB_PORT
# ENV REDIS_HOST
# ENV REDIS_DB
