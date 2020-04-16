FROM node:latest

ENV APP_ROOT /src

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

ADD ./frontend/package.json ${APP_ROOT}/package.json
RUN npm install
ADD . ${APP_ROOT}
