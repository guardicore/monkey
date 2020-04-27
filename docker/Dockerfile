FROM debian:stretch-slim

LABEL MAINTAINER="theonlydoo <theonlydoo@gmail.com>"

ARG RELEASE=1.8.0
ARG DEBIAN_FRONTEND=noninteractive

EXPOSE 5000

WORKDIR /app

ADD https://github.com/guardicore/monkey/releases/download/${RELEASE}/infection_monkey_deb.${RELEASE}.tgz .

RUN tar xvf infection_monkey_deb.${RELEASE}.tgz  \
    && apt-get -yqq update                       \
    && apt-get -yqq upgrade                      \
    && apt-get -yqq install python-pip           \
                            python-dev           \
    && dpkg -i *.deb                             \
    && rm -f *.deb *.tgz

WORKDIR /var/monkey
ENTRYPOINT ["/var/monkey/monkey_island/bin/python/bin/python"]
CMD ["/var/monkey/monkey_island.py"]
