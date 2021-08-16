#!/usr/bin/env python3

from gcp_test_machine_list import GCP_TEST_MACHINE_LIST
from utils.gcp_machine_handlers import GCPHandler

gcp_handler = GCPHandler()
gcp_handler.stop_machines(" ".join(GCP_TEST_MACHINE_LIST))
