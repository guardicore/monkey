import BaseConfig from './BaseConfig';

class StandardConfig extends BaseConfig {

  isAuthEnabled() {
    return false;
  }
}

export default StandardConfig;
