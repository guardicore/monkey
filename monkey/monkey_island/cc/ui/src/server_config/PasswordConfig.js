import BaseConfig from './BaseConfig';

class PasswordConfig extends BaseConfig {
  isAuthEnabled() {
    return true;
  }
}

export default PasswordConfig;
