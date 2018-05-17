FROM debian:jessie-slim

LABEL MAINTAINER="theonlydoo <theonlydoo@gmail.com>"

WORKDIR /app

ADD https://github.com/guardicore/monkey/releases/download/1.5.2/infection_monkey_1.5.2_deb.tgz .

RUN tar xvf infection_monkey_1.5.2_deb.tgz  \
    && apt-get -yqq update                  \
    && apt-get -yqq upgrade                 \
    && apt-get -yqq install python-pip      \
                            libssl-dev      \
                            supervisor      \
    && dpkg -i *.deb    

COPY stack.conf /etc/supervisor/conf.d/stack.conf

ENTRYPOINT [ "supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf" ]