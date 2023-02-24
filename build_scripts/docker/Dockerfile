ARG PYTHON_VERSION=3.11
# Install python dependencies using the bitnami/python:3.7 image, which includes
# development dependencies.
FROM python:$PYTHON_VERSION-slim as builder
COPY ./monkey /monkey
WORKDIR /monkey
RUN apt-get update && apt-get install -y gcc
RUN python -m venv .
RUN export CI=1
RUN . bin/activate && \
    pip install -U pip && \
    cd monkey_island && \
    pip install pipenv && \
    pipenv sync


# Build the final application using a second image, which
# does not include development dependencies.
FROM python:$PYTHON_VERSION-slim
COPY --from=builder /monkey /monkey
WORKDIR /monkey
EXPOSE 5000
ENV MONKEY_DOCKER_CONTAINER=true
RUN apt-get update && apt-get install -y iputils-ping && apt-get clean
RUN groupadd -r monkey-island && useradd --no-log-init -r -g monkey-island monkey-island
RUN chmod 444 /monkey/monkey_island/cc/server.key
RUN chmod 444 /monkey/monkey_island/cc/server.csr
RUN chmod 444 /monkey/monkey_island/cc/server.crt
RUN mkdir /monkey_island_data && chmod 700 /monkey_island_data && chown -R monkey-island:monkey-island /monkey_island_data
USER monkey-island
ENTRYPOINT ["/monkey/entrypoint.sh"]
