export function reformatConfig(config, reverse = false) {
    if (reverse) {
      config['payloads'] = [{'name': 'ransomware', 'options': config['payloads']}]
    } else {
      config['payloads'] = config['payloads'][0]['options'];
    }
    return config;
  }
