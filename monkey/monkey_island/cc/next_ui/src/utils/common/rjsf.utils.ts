const findSchemaPath = (rootSchema: any, schema: any, parts: string[]) => {
    const properties = rootSchema?.properties;
    if (!properties || typeof properties !== 'object') {
        return false;
    }

    for (const property of Object.keys(properties)) {
        parts.push(property);
        if (schema === properties[property]) {
            return parts;
        }
        if (findSchemaPath(properties[property], schema, parts)) {
            return true;
        }
        parts.pop();
    }
    return false;
};

// Given a schema, return the path to that schema in the root schema
export const getSchemaPath = (rootSchema: any, schema: any) => {
    const parts: string[] = [];

    findSchemaPath(rootSchema, schema, parts);
    return parts;
};

// Given a schema, return the sub-schema at the given path
// path is a dot-separated string
export const getSubSchema = (schema: any, path: string) => {
    const parts = path.split('.');
    let subSchema = schema;
    for (const part of parts) {
        if (
            !subSchema.properties ||
            typeof subSchema.properties !== 'object' ||
            !(part in subSchema.properties)
        ) {
            return {};
        }
        subSchema = subSchema.properties[part];
    }
    return subSchema;
};
