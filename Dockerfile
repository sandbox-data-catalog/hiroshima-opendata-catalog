# See CKAN docs on installation from Docker Compose on usage
FROM debian:jessie

# Install required system packages
RUN apt-get -q -y update \
    && DEBIAN_FRONTEND=noninteractive apt-get -q -y upgrade \
    && apt-get -q -y install \
        python-dev \
        python-pip \
        python-virtualenv \
        python-wheel \
        libpq-dev \
        libxml2-dev \
        libxslt-dev \
        libgeos-dev \
        libssl-dev \
        libffi-dev \
        postgresql-client \
        build-essential \
        git-core \
        vim \
        wget \
        apache2 \
        libapache2-mod-wsgi \
        libapache2-mod-rpaf \
        jq \
        curl \
    && apt-get -q clean \
    && rm -rf /var/lib/apt/lists/*

# Define environment variables
ENV CKAN_HOME /usr/lib/ckan
ENV CKAN_VENV $CKAN_HOME/venv
ENV CKAN_CONFIG /etc/ckan

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2

# Build-time variables specified by docker-compose.yml / .env
ARG CKAN_SITE_URL
ARG CKAN_STORAGE_PATH
ARG USE_CKAN_CONFIG_NAME

# Create ckan user
#RUN useradd -r -u 900 -m -c "ckan account" -d $CKAN_HOME -s /bin/false ckan

# Setup virtual environment for CKAN
RUN mkdir -p $CKAN_VENV $CKAN_CONFIG $CKAN_STORAGE_PATH && \
    virtualenv $CKAN_VENV && \
    ln -s $CKAN_VENV/bin/pip /usr/local/bin/ckan-pip && \
    ln -s $CKAN_VENV/bin/python /usr/local/bin/ckan-python &&\
    ln -s $CKAN_VENV/bin/paster /usr/local/bin/ckan-paster

# Setup CKAN
COPY . $CKAN_VENV/src/ckan/
RUN ckan-pip install -U pip && \
    ckan-pip install --upgrade --no-cache-dir -r $CKAN_VENV/src/ckan/requirement-setuptools.txt && \
    ckan-pip install --upgrade --no-cache-dir -r $CKAN_VENV/src/ckan/requirements.txt && \
    ckan-pip install -e $CKAN_VENV/src/ckan/ && \
    cd $CKAN_VENV/src/ckan/ckanext-hiroshima/ && \
    ckan-python $CKAN_VENV/src/ckan/ckanext-hiroshima/setup.py develop && \
    cp -v $CKAN_VENV/src/ckan/contrib/docker/ckan-entrypoint.sh /ckan-entrypoint.sh && \
    chmod +x /ckan-entrypoint.sh && \
    ln -s $CKAN_VENV/src/ckan/ckan/config/who.ini $CKAN_CONFIG/who.ini && \
    chown -R $APACHE_RUN_GROUP:$APACHE_RUN_USER $CKAN_HOME $CKAN_VENV $CKAN_CONFIG $CKAN_STORAGE_PATH

COPY ckan/config/$USE_CKAN_CONFIG_NAME /etc/ckan/ckan.ini
COPY contrib/docker/apache.wsgi /etc/ckan/apache.wsgi
COPY contrib/docker/apache/apache2.conf /etc/apache2/apache2.conf
COPY contrib/docker/apache/ports.conf /etc/apache2/ports.conf
COPY contrib/docker/apache/sites-available/ckan.conf /etc/apache2/sites-available/ckan.conf

RUN a2ensite ckan && a2dissite 000-default

RUN mkdir -p $APACHE_RUN_DIR && \
    mkdir -p $APACHE_LOG_DIR && \
    mkdir -p $APACHE_LOCK_DIR && \
    chown -R $APACHE_RUN_GROUP:$APACHE_RUN_USER $APACHE_RUN_DIR && \
    chown -R $APACHE_RUN_GROUP:$APACHE_RUN_USER $APACHE_LOG_DIR && \
    chown -R $APACHE_RUN_GROUP:$APACHE_RUN_USER $APACHE_LOCK_DIR

USER $APACHE_RUN_USER
EXPOSE 5000

ENTRYPOINT ["/ckan-entrypoint.sh"]
CMD ["apache2ctl", "-D", "FOREGROUND"]
