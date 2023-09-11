#!/bin/sh

ROOT="$( cd "$( dirname "$0" )" && pwd )"

printerr() {
    echo "$@" >&2
}

show_usage() {
    printerr "Usage: $0 [OPTIONS] FILE..."
    printerr "Options:"
    printerr "  -p|--project-id <project_id>  GCP project ID (required)"
    printerr "  --account-file <file>         GCP service account file (required)"
    printerr "  -f|--force                    Force build even if image already exists"
    printerr "  -d|--debug                    Leave the instance running for debugging"
    printerr "  -h|--help                     Show this help message and exit"
}

# Read options
PROJECT_ID=
ACCOUNT_FILE=
FORCE=
DEBUG=

while :; do
    case $1 in
        -h|-\?|--help)
            show_usage
            exit
            ;;
        -p|--project-id)
            if [ "$2" ]; then
                PROJECT_ID=$2
                shift 2
            else
                printerr 'ERROR: "--project-id" requires a non-empty option argument.\n'
                exit 1
            fi
            ;;
        --account-file)
            if [ "$2" ]; then
                ACCOUNT_FILE=$(realpath "$2")
                shift 2
            else
                printerr 'ERROR: "--account-file" requires a non-empty option argument.\n'
                exit 1
            fi
            ;;
        -f|--force)
            FORCE=-force
            shift
            ;;
        -d|--debug)
            DEBUG=-debug
            shift
            ;;
        *)
            break
    esac
done

if [ -z "$PROJECT_ID" ]; then
    printerr "ERROR: --project-id is required"
    show_usage
    exit 1
fi

if [ -z "$ACCOUNT_FILE" ]; then
    printerr "ERROR: --account-file is required"
    show_usage
    exit 1
fi

prevdir=$(pwd)
cd "$ROOT" || exit 1
for file in "$@"; do
    if file_path=$(realpath -q "$file") && [ -f "$file_path" ]; then
        packer build $FORCE $DEBUG -on-error=ask -var "project_id=$PROJECT_ID" -var "account_file=$ACCOUNT_FILE" "$file_path"
    elif file_path=$(realpath -q "$prevdir/$file") && [ -f "$file_path" ]; then
        packer build $FORCE $DEBUG -on-error=ask -var "project_id=$PROJECT_ID" -var "account_file=$ACCOUNT_FILE" "$file_path"
    else
        printerr "File does not exist: '$file'. Skipping."
    fi
done
cd "$prevdir" || exit 1
