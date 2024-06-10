#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
docker buildx build --platform linux/arm64,linux/amd64 --tag infectionmonkey/ssh1 --push - < "$SCRIPT_DIR/ssh1.dockerfile"
docker buildx build --load --platform linux/arm64 --tag infectionmonkey/ssh1 - < "$SCRIPT_DIR/ssh1.dockerfile"
docker buildx build --load --platform linux/amd64 --tag infectionmonkey/ssh1 - < "$SCRIPT_DIR/ssh1.dockerfile"
