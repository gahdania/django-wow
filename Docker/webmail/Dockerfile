FROM alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache apk add lighttpd php php-pgsql php-imap

RUN /etc/init.d/mini_httpd stop

RUN apk del mini_httpd
RUN mkdir -p /var/www/domains/gahd.io/www
RUN ln -s /usr/share/acf/www /var/www/domains/gahd.io/www

RUN sed

COPY index.html /var/www/domains/gahd.io/www/index.html


