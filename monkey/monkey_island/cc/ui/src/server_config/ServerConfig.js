import StandardConfig from './StandardConfig';
import AwsConfig from './AwsConfig';

const SERVER_CONFIG_JSON = require('../../../server_config.json');

const CONFIG_DICT =
  {
    'standard': StandardConfig,
    'aws': AwsConfig
  };

export const SERVER_CONFIG = new CONFIG_DICT[SERVER_CONFIG_JSON['server_config']]();
