FROM ubuntu:xenial
MAINTAINER james.wilkins@fasthosts.co.uk
ARG DEBIAN_FRONTEND=noninteractive
COPY files/ /
RUN \
  apt-get -y update && \
  apt-get -o Dpkg::Options::=--force-confdef -y install supervisor curl vim bzip2 ssmtp && \
  locale-gen en_GB.utf8 en_US.utf8 es_ES.utf8 de_DE.UTF-8 && \
  mkdir --mode 777 -p /var/log/supervisor && \
  chmod -R 777 /var/run /var/log && \
  mkdir --mode 777 -p /tmp/sockets && \
  chmod -R 755 /init /hooks && \
  chmod 755 /etc/supervisor/exit_on_fatal.py && \
  apt-get -y clean && \
  rm -rf /var/lib/apt/lists/*
ENV \
  SUPERVISORD_EXIT_ON_FATAL=1 \
  LC_ALL=en_GB.UTF-8 \
  LANG=en_GB.UTF-8 \
  LANGUAGE=en_GB.UTF-8
ENTRYPOINT ["/bin/bash", "-e", "/init/entrypoint"]
CMD ["run"]
