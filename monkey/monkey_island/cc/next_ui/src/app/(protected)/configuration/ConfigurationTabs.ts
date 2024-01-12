export enum ConfigurationTabs {
    Propagation = 'propagation',
    Payloads = 'payloads',
    CredentialsCollectors = 'credentials_collectors',
    Masquerade = 'masquerade',
    Polymorphism = 'polymorphism',
    Advanced = 'advanced'
}

const CONFIGURATION_TABS_ORDER = [
    ConfigurationTabs.Propagation,
    ConfigurationTabs.Payloads,
    ConfigurationTabs.CredentialsCollectors,
    ConfigurationTabs.Masquerade,
    ConfigurationTabs.Polymorphism,
    ConfigurationTabs.Advanced
];

export default CONFIGURATION_TABS_ORDER;
