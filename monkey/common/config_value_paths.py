AWS_KEYS_PATH = ["internal", "monkey", "aws_keys"]
EXPORT_MONKEY_TELEMS_PATH = ["internal", "testing", "export_monkey_telems"]
CURRENT_SERVER_PATH = ["internal", "island_server", "current_server"]
SSH_KEYS_PATH = ["internal", "exploits", "exploit_ssh_keys"]
INACCESSIBLE_SUBNETS_PATH = ["basic_network", "network_analysis", "inaccessible_subnets"]
USER_LIST_PATH = ["basic", "credentials", "exploit_user_list"]
PASSWORD_LIST_PATH = ["basic", "credentials", "exploit_password_list"]
EXPLOITER_CLASSES_PATH = ["basic", "exploiters", "exploiter_classes"]
SUBNET_SCAN_LIST_PATH = ["basic_network", "scope", "subnet_scan_list"]
LOCAL_NETWORK_SCAN_PATH = ["basic_network", "scope", "local_network_scan"]
LM_HASH_LIST_PATH = ["internal", "exploits", "exploit_lm_hash_list"]
NTLM_HASH_LIST_PATH = ["internal", "exploits", "exploit_ntlm_hash_list"]

# TODO: These are tuples so that they are immutable. Make the rest of these paths tuples as well.
PBA_LINUX_FILENAME_PATH = ("monkey", "post_breach", "PBA_linux_filename")
PBA_WINDOWS_FILENAME_PATH = ("monkey", "post_breach", "PBA_windows_filename")
