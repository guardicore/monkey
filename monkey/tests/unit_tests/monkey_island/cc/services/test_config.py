from monkey_island.cc.services.config import ConfigService

# If tests fail because config path is changed, sync with
# monkey/monkey_island/cc/ui/src/components/pages/RunMonkeyPage/RunOptions.js


def test_get_config_propagation_credentials_from_flat_config(flat_monkey_config):
    expected_creds = {
        "exploit_lm_hash_list": ["lm_hash_1", "lm_hash_2"],
        "exploit_ntlm_hash_list": ["nt_hash_1", "nt_hash_2", "nt_hash_3"],
        "exploit_password_list": ["test", "iloveyou", "12345"],
        "exploit_ssh_keys": [{"private_key": "my_private_key", "public_key": "my_public_key"}],
        "exploit_user_list": ["Administrator", "root", "user", "ubuntu"],
    }

    creds = ConfigService.get_config_propagation_credentials_from_flat_config(flat_monkey_config)
    assert creds == expected_creds
