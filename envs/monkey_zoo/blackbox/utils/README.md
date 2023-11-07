# BlackBox utility scripts

## Config generation script

This script is used to generate config files for manual tests.
Config file will be generated according to the templates in `envs/monkey_zoo/blackbox/config_templates`.

1. Reset the Island config to contain default configuration.
2. Run `envs/monkey_zoo/blackbox/utils/config_generation_script.py island_ip:5000` to populate
`envs/monkey_zoo/blackbox/utils/generated_configs` directory with configuration files.

!! It's important to target the Island you'll be testing, because configs contain Island's IPs
in the configuration !!
