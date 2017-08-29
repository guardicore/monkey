'use strict';

import baseConfig from './base';

let config = {
  appEnv: 'dist'  // feel free to remove the appEnv property here
};

export default Object.freeze(Object.assign({}, baseConfig, config));
