FROM nginx:latest
MAINTAINER Tomasz Skibinski <tomasz.skibinski@linxsys.pl>

WORKDIR /usr/share/nginx

# Update and upgrade for security
RUN apt-get update -yq \
    && apt-get upgrade -y \
    && apt-get install -y php5-fpm php5-mysql curl

RUN curl -L https://files.phpmyadmin.net/phpMyAdmin/4.5.1/phpMyAdmin-4.5.1-all-languages.tar.gz | tar -xzf- \
  && chown -R nginx:nginx phpMyAdmin* \
  && ln -s phpMyAdmin-* phpmyadmin \
  && mv phpmyadmin/config.sample.inc.php phpmyadmin/config.inc.php

RUN sed -i '1a daemon off;' /etc/nginx/nginx.conf \
  && rm -f /etc/nginx/conf.d/default.conf /var/log/nginx/* \
  && sed -i 's/www-data/nginx/g' /etc/php5/fpm/pool.d/www.conf \
  && sed -i 's/^pm.max_children.*/pm.max_children = 2/g' /etc/php5/fpm/pool.d/www.conf \
  && sed -i 's/^pm.start_servers.*/pm.start_servers = 1/g' /etc/php5/fpm/pool.d/www.conf \
  && sed -i 's/^pm.max_spare_servers.*/pm.max_spare_servers = 2/g' /etc/php5/fpm/pool.d/www.conf \
  && sed -i 's/^upload_max_filesize.*/upload_max_filesize = 128M/g' /etc/php5/fpm/php.ini \
  && sed -i 's/^post_max_size.*/post_max_size = 128M/g' /etc/php5/fpm/php.ini

COPY pma.conf /etc/nginx/conf.d/
COPY pma_run /usr/sbin/pma_run

# Clean cache and temp files
RUN apt-get clean -qy \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*

ENTRYPOINT [ "/usr/sbin/pma_run" ]
