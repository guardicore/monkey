import argparse
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List

import mongoengine
import pymongo
from attack_mitigations import AttackMitigations
from bson import json_util
from stix2 import AttackPattern, CourseOfAction, FileSystemSource, Filter

COLLECTION_NAME = "attack_mitigations"


def main():
    args = parse_args()

    set_default_mongo_connection(args.database_name, args.mongo_host, args.mongo_port)

    mongo_client = pymongo.MongoClient(host=args.mongo_host, port=args.mongo_port)
    database = mongo_client.get_database(args.database_name)

    clean_collection(database)
    populate_attack_mitigations(database, Path(args.cti_repo))
    dump_attack_mitigations(database, Path(args.cti_repo), Path(args.dump_file_path))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export attack mitigations from a database",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mongo_host", default="localhost", help="URL for mongo database.", required=False
    )
    parser.add_argument(
        "--mongo-port",
        action="store",
        default=27017,
        type=int,
        help="Port for mongo database.",
        required=False,
    )
    parser.add_argument(
        "--database-name",
        action="store",
        default="monkeyisland",
        help="Database name inside of mongo.",
        required=False,
    )
    parser.add_argument(
        "--cti-repo",
        action="store",
        default="attack_mitigations",
        help="The path to the Cyber Threat Intelligence Repository.",
        required=True,
    )
    parser.add_argument(
        "--dump-file-path",
        action="store",
        default="./attack_mitigations.json",
        help="A file path where the database dump will be saved.",
        required=False,
    )

    return parser.parse_args()


def set_default_mongo_connection(database_name: str, host: str, port: int):
    mongoengine.connect(db=database_name, host=host, port=port)


def clean_collection(database: pymongo.database.Database):
    if collection_exists(database, COLLECTION_NAME):
        database.drop_collection(COLLECTION_NAME)


def collection_exists(database: pymongo.database.Database, collection_name: str) -> bool:
    return collection_name in database.list_collection_names()


def populate_attack_mitigations(database: pymongo.database.Database, cti_repo: Path):
    database.create_collection(COLLECTION_NAME)
    attack_data_path = cti_repo / "enterprise-attack"

    stix2_mitigations = get_all_mitigations(attack_data_path)
    mongo_mitigations = AttackMitigations.dict_from_stix2_attack_patterns(
        get_all_attack_techniques(attack_data_path)
    )
    mitigation_technique_relationships = get_technique_and_mitigation_relationships(
        attack_data_path
    )
    for relationship in mitigation_technique_relationships:
        mongo_mitigations[relationship["target_ref"]].add_mitigation(
            stix2_mitigations[relationship["source_ref"]]
        )
    for relationship in mitigation_technique_relationships:
        mongo_mitigations[relationship["target_ref"]].add_no_mitigations_info(
            stix2_mitigations[relationship["source_ref"]]
        )
    for key, mongo_object in mongo_mitigations.items():
        mongo_object.save()


def get_all_mitigations(attack_data_path: Path) -> Dict[str, CourseOfAction]:
    file_system = FileSystemSource(attack_data_path)
    mitigation_filter = [Filter("type", "=", "course-of-action")]
    all_mitigations = file_system.query(mitigation_filter)
    all_mitigations = {mitigation["id"]: mitigation for mitigation in all_mitigations}
    return all_mitigations


def get_all_attack_techniques(attack_data_path: Path) -> Dict[str, AttackPattern]:
    file_system = FileSystemSource(attack_data_path)
    technique_filter = [Filter("type", "=", "attack-pattern")]
    all_techniques = file_system.query(technique_filter)
    all_techniques = {technique["id"]: technique for technique in all_techniques}
    return all_techniques


def get_technique_and_mitigation_relationships(attack_data_path: Path) -> List[CourseOfAction]:
    file_system = FileSystemSource(attack_data_path)
    technique_filter = [
        Filter("type", "=", "relationship"),
        Filter("relationship_type", "=", "mitigates"),
    ]
    all_techniques = file_system.query(technique_filter)
    return all_techniques


def dump_attack_mitigations(
    database: pymongo.database.Database, cti_repo: Path, dump_file_path: Path
):
    if not collection_exists(database, COLLECTION_NAME):
        raise Exception(f"Could not find collection: {COLLECTION_NAME}")

    metadata = get_metadata(cti_repo)
    data = get_data_from_database(database)

    json_output = f'{{"metadata":{json.dumps(metadata)},"data":{json_util.dumps(data)}}}'

    with open(dump_file_path, "wb") as jsonfile:
        jsonfile.write(json_output.encode())


def get_metadata(cti_repo: Path) -> dict:
    timestamp = str(time.time())
    commit_hash = get_commit_hash(cti_repo)
    origin_url = get_origin_url(cti_repo)

    return {"timestamp": timestamp, "commit_hash": commit_hash, "origin_url": origin_url}


def get_commit_hash(cti_repo: Path) -> str:
    return run_command(["git", "rev-parse", "--short", "HEAD"], cti_repo).strip()


def get_origin_url(cti_repo: Path) -> str:
    return run_command(["git", "remote", "get-url", "origin"], cti_repo).strip()


def run_command(cmd: List, cwd: Path = None) -> str:
    cp = subprocess.run(cmd, capture_output=True, cwd=cwd, encoding="utf-8")

    if cp.returncode != 0:
        raise Exception(
            f"Error running command -- Command: {cmd} -- Return Code: {cp.returncode} -- stderr: "
            f"{cp.stderr}"
        )

    return cp.stdout


def get_data_from_database(database: pymongo.database.Database) -> pymongo.cursor.Cursor:
    collection = database.get_collection(COLLECTION_NAME)
    collection_contents = collection.find()

    return collection_contents


if __name__ == "__main__":
    main()
