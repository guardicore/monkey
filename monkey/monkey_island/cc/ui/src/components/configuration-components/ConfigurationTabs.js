const CONFIGURATION_TABS = {
  BASIC: 'basic',
  BASIC_NETWORK: 'basic_network',
  RANSOMWARE: 'ransomware',
  MONKEY: 'monkey',
  INTERNAL: 'internal'
};

const advancedModeConfigTabs = [
  CONFIGURATION_TABS.BASIC,
  CONFIGURATION_TABS.BASIC_NETWORK,
  CONFIGURATION_TABS.RANSOMWARE,
  CONFIGURATION_TABS.MONKEY,
  CONFIGURATION_TABS.INTERNAL
];

const ransomwareModeConfigTabs = [
  CONFIGURATION_TABS.BASIC,
  CONFIGURATION_TABS.BASIC_NETWORK,
  CONFIGURATION_TABS.RANSOMWARE
];

const CONFIGURATION_TABS_PER_MODE = {
  'advanced': advancedModeConfigTabs,
  'ransomware': ransomwareModeConfigTabs
};

export default CONFIGURATION_TABS_PER_MODE;
