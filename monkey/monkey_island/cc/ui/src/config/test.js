'use strict';

import baseConfig from './base';

let config = {
  appEnv: 'test'  // don't remove the appEnv property here
};

export default Object.freeze(Object.assign(baseConfig, config));
