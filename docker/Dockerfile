FROM debian:jessie-slim

LABEL MAINTAINER="theonlydoo <theonlydoo@gmail.com>"

ARG RELEASE=1.6

WORKDIR /app

ADD https://github.com/guardicore/monkey/releases/download/${RELEASE}/infection_monkey_deb.${RELEASE}.tgz .

RUN tar xvf infection_monkey_deb.${RELEASE}.tgz  \
    && apt-get -yqq update                       \
    && apt-get -yqq upgrade                      \
    && apt-get -yqq install python-pip           \
                            libssl-dev           \
                            supervisor           \
    && dpkg -i *.deb

COPY stack.conf /etc/supervisor/conf.d/stack.conf

ENTRYPOINT [ "supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf" ]