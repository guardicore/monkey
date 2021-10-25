import os

# Must match evn var name in build_scripts/docker/Dockerfile:21
DOCKER_ENV_VAR = "MONKEY_DOCKER_CONTAINER"


def is_running_on_docker():
    return os.environ.get(DOCKER_ENV_VAR) == "true"
