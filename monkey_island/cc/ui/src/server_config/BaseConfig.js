class BaseConfig {

  isAuthEnabled() {
    throw new Error('Abstract function');
  }
}

export default BaseConfig;
