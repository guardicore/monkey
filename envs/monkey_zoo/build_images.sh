#!/bin/sh

ROOT="$( cd "$( dirname "$0" )" && pwd )"

printerr() {
    echo "$@" >&2
}

show_usage() {
    printerr "Usage: $0 [options]"
    printerr "Options:"
    printerr "  -p|--project-id <project_id>  GCP project ID (required)"
    printerr "  --account-file <file>         GCP service account file (required)"
    printerr "  -f|--force                    Force build even if image already exists"
    printerr "  -h|--help                     Show this help message and exit"
}

# Read options
PROJECT_ID=
ACCOUNT_FILE=
FORCE=

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
                ACCOUNT_FILE=$2
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

packer build $FORCE -var "project_id=$PROJECT_ID" -var "account_file=$ACCOUNT_FILE" "$ROOT/packer/snmp.pkr.hcl"
