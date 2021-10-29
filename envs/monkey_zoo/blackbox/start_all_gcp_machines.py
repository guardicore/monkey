#!/usr/bin/env python3

from gcp_test_machine_list import GCP_TEST_MACHINE_LIST
from utils.gcp_machine_handlers import initialize_gcp_client, start_machines

initialize_gcp_client()
start_machines(GCP_TEST_MACHINE_LIST)
