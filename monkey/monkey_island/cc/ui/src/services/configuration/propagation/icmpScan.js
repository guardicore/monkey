const ICMP_SCAN_CONFIGURATION_SCHEMA = {
    title: 'Ping scanner',
    type: 'object',
    properties: {
        timeout: {
            title: 'Ping scan timeout',
            type: 'number',
            minimum: 0.0,
            description: 'Maximum time to wait for ping response in seconds'
        }
    }
};

export default ICMP_SCAN_CONFIGURATION_SCHEMA;
