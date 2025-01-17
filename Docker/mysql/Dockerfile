FROM mysql:8.0-debian

WORKDIR /app_db
RUN apt-get -y update && \
    apt-get -y install python3-dev default-libmysqlclient-dev build-essential pkg-config

CMD ["bash"]