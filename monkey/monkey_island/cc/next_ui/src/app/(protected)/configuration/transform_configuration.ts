import _ from 'lodash';

const CONFIG_MAPPINGS = [
    {
        from: 'propagation.general.maximum_depth',
        to: 'propagation.maximum_depth'
    },
    { from: 'advanced.keep_tunnel_open_time', to: 'keep_tunnel_open_time' }
];

function invertMappings(mappings) {
    return mappings.map((mapping) => {
        return {
            from: mapping.to,
            to: mapping.from
        };
    });
}

function reformatConfig(config, mappings, reverse = false) {
    const formattedConfig = _.cloneDeep(config);
    let configMapping = _.cloneDeep(mappings);

    if (reverse) {
        configMapping = invertMappings(configMapping);
    }

    configMapping.forEach((mapping) => {
        const value = _.get(formattedConfig, mapping.from);
        _.set(formattedConfig, mapping.to, value);
        _.unset(formattedConfig, mapping.from);
    });

    return formattedConfig;
}

export default function transformConfiguration(config, reverse = false) {
    return reformatConfig(config, CONFIG_MAPPINGS, reverse);
}
