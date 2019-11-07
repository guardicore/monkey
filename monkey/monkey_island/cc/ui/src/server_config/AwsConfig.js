import BaseConfig from './BaseConfig';

class AwsConfig extends BaseConfig {
  isAuthEnabled() {
    return true;
  }
}

export default AwsConfig;
