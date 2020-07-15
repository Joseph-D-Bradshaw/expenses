FROM postgres
ENV POSTGRES_PASSWORD developmentpassword
ENV POSTGRES_DB developmentdb
COPY init.sql /docker-entrypoint-initdb.d/