export const pluginConfigurationSchema = {
    type: 'object',
    properties: {
        name: {
            title: 'Name',
            type: 'string'
        },
        safe: {
            type: 'boolean'
        },
        options: {
            type: 'object'
        }
    }
};
