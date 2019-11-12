import StandardConfig from './StandardConfig';
import AwsConfig from './AwsConfig';
import PasswordConfig from './PasswordConfig';

const SERVER_CONFIG_JSON = require('../../../server_config.json');

const CONFIG_DICT =
  {
    'standard': StandardConfig,
    'aws': AwsConfig,
    'password': PasswordConfig
  };

export const SERVER_CONFIG = new CONFIG_DICT[SERVER_CONFIG_JSON['server_config']]();
