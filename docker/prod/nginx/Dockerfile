FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY ./docker/prod/nginx/backend.conf /etc/nginx/conf.d/