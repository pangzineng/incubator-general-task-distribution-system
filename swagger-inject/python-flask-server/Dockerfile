FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN apk --update add --virtual build-dependencies build-base \
  && pip3 install --no-cache-dir -r requirements.txt \
  && apk del build-dependencies

COPY . /usr/src/app

EXPOSE 8080

CMD [ "gunicorn", "--workers=4",  "--bind", "0.0.0.0:8080", "swagger_server.__main__:app" ]
