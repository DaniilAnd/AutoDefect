FROM postgres:14

EXPOSE 5432

COPY ./init_db.sh /docker-entrypoint-initdb.d/init_db.sh

CMD /docker-entrypoint-initdb.d/init_db.sh