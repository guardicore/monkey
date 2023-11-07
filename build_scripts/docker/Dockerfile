ARG PYTHON_VERSION=3.11
# Install python and some build dependencies
FROM python:$PYTHON_VERSION-slim as builder
COPY ./monkey /monkey
WORKDIR /monkey
RUN python -m venv . \
    && export CI=1 \
    && . bin/activate \
    && pip install -U pip \
    && cd monkey_island \
    && pip install pipenv \
    && pipenv sync


# Build the final application using a second image, which
# does not include development dependencies.
FROM python:$PYTHON_VERSION-slim
COPY --from=builder /monkey /monkey
WORKDIR /monkey
EXPOSE 5000
EXPOSE 443
ENV MONKEY_DOCKER_CONTAINER=true
RUN apt-get update \
    && apt-get install -y iputils-ping \
    && apt-get clean \
    && groupadd -r monkey-island \
    && useradd --no-log-init -r -g monkey-island monkey-island \
    && chmod 444 /monkey/monkey_island/cc/server.key \
    && chmod 444 /monkey/monkey_island/cc/server.csr \
    && chmod 444 /monkey/monkey_island/cc/server.crt \
    && mkdir /monkey_island_data \
    && chmod 700 /monkey_island_data \
    && chown -R monkey-island:monkey-island /monkey_island_data \
    && setcap 'cap_net_bind_service=+ep' /monkey/monkey_island/bin/node/node

USER monkey-island
ENTRYPOINT ["/monkey/entrypoint.sh"]
