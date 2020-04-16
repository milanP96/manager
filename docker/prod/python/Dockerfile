FROM python:3.7

COPY ./backend /backend

WORKDIR /backend

RUN pip install -r requirements/prod.txt

COPY ./docker/prod/python/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]