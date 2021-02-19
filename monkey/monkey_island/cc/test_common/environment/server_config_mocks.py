# Username:test Password:test
CONFIG_WITH_CREDENTIALS = {
    "server_config": "password",
    "deployment": "develop",
    "user": "test",
    "password_hash": "9ece086e9bac491fac5c1d1046ca11d737b92a2b2ebd93f005d7b710110c0a678288166e7fbe796883a"
                     "4f2e9b3ca9f484f521d0ce464345cc1aec96779149c14"
}

CONFIG_NO_CREDENTIALS = {
    "server_config": "password",
    "deployment": "develop"
}

CONFIG_PARTIAL_CREDENTIALS = {
    "server_config": "password",
    "deployment": "develop",
    "user": "test"
}

CONFIG_BOGUS_VALUES = {
    "server_config": "password",
    "deployment": "develop",
    "user": "test",
    "aws": "test",
    "test": "test",
    "test2": "test2"
}

CONFIG_STANDARD_ENV = {
    "server_config": "standard",
    "deployment": "develop"
}

CONFIG_STANDARD_WITH_CREDENTIALS = {
    "server_config": "standard",
    "deployment": "develop",
    "user": "test",
    "password_hash": "9ece086e9bac491fac5c1d1046ca11d737b92a2b2ebd93f005d7b710110c0a678288166e7fbe796883a"
                     "4f2e9b3ca9f484f521d0ce464345cc1aec96779149c14"
}
