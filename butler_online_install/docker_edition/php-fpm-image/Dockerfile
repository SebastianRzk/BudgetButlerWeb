FROM php:7-fpm
RUN apt-get update &&\
    apt-get install -y libpq-dev &&\
    docker-php-ext-install pdo pdo_mysql pdo_pgsql &&\
    rm -rf /var/lib/apt/lists/* &&\
    apt-get clean
