import mergeAllOf from 'json-schema-merge-allof';
import $RefParser from '@apidevtools/json-schema-ref-parser';
import { MASQUERADE } from '@/app/(protected)/configuration/masquerade';

function reorderProperties(schema) {
    const originalProperties = schema['properties'];
    const reorderedProperties = {
        propagation: null,
        payloads: null,
        credentials_collectors: null,
        masquerade: null,
        polymorphism: null,
        advanced: null
    };
    schema['properties'] = Object.assign(
        reorderedProperties,
        originalProperties
    );
}

function reformatSchema(schema) {
    schema['properties']['propagation']['properties']['credentials'] = {
        title: 'Credentials'
    };
    schema['properties']['masquerade'] = MASQUERADE;
    schema['properties']['propagation']['properties']['general'] = {
        title: 'General',
        type: 'object',
        properties: {
            maximum_depth:
                schema['properties']['propagation']['properties'][
                    'maximum_depth'
                ]
        }
    };
    delete schema['properties']['propagation']['properties']['maximum_depth'];
    schema['properties']['advanced'] = {
        title: 'Advanced',
        type: 'object',
        properties: {
            keep_tunnel_open_time: schema['properties']['keep_tunnel_open_time']
        }
    };
    delete schema['properties']['keep_tunnel_open_time'];
    delete schema['$defs'];
    reorderProperties(schema);
    return schema;
}

export default async function transformSchema(schema) {
    const transformedSchema = await $RefParser
        .dereference(schema)
        .then((schema) => {
            schema = mergeAllOf(schema);
            return reformatSchema(schema);
        });
    return transformedSchema;
}
