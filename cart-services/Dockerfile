FROM php:8.2-cli
WORKDIR /var/www/html
COPY . .
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && docker-php-ext-install pdo pdo_pgsql
EXPOSE 3002
CMD [ "php", "-S", "0.0.0.0:3002", "-t", "public" ]
