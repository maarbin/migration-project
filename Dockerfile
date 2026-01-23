FROM postgres:15

COPY ./db/init/ /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/*.sh