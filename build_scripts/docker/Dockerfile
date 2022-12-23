# Install python dependencies using the bitnami/python:3.7 image, which includes
# development dependencies.
FROM bitnami/python:3.7 as builder
COPY ./monkey /monkey
WORKDIR /monkey
RUN virtualenv .
RUN export CI=1
RUN . bin/activate && \
    cd monkey_island && \
    pip install pipenv==2022.7.4 && \
    pipenv sync


# Build the final application using the bitnami/python:3.7-prod image, which
# does not include development dependencies.
FROM bitnami/python:3.7-prod
RUN apt-get update && apt-get install -y iputils-ping && apt-get clean
COPY --from=builder /monkey /monkey
WORKDIR /monkey
EXPOSE 5000
ENV MONKEY_DOCKER_CONTAINER=true
RUN groupadd -r monkey-island && useradd --no-log-init -r -g monkey-island monkey-island
RUN chmod 444 /monkey/monkey_island/cc/server.key
RUN chmod 444 /monkey/monkey_island/cc/server.csr
RUN chmod 444 /monkey/monkey_island/cc/server.crt
RUN mkdir /monkey_island_data && chmod 700 /monkey_island_data && chown -R monkey-island:monkey-island /monkey_island_data
USER monkey-island
ENTRYPOINT ["/monkey/entrypoint.sh"]
