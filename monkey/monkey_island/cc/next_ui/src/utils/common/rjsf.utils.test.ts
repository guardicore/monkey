import { describe, expect, test } from '@jest/globals';
import { getSchemaPath, getSubSchema } from './rjsf.utils';

describe('getSchemaPath', () => {
    test('Empty if no root schema us null', () => {
        const result = getSchemaPath(null, {});
        expect(result).toEqual([]);
    });
    test('Empty if no properties', () => {
        const result = getSchemaPath({}, {});
        expect(result).toEqual([]);
    });
    test('Empty if no match', () => {
        const result = getSchemaPath({ properties: {} }, {});
        expect(result).toEqual([]);
    });
    test('Single property', () => {
        const schema = { properties: { a: {} } };
        const result = getSchemaPath(schema, schema.properties.a);
        expect(result).toEqual(['a']);
    });
    test('Nested property', () => {
        const schema = { properties: { a: { properties: { b: {} } } } };
        const result = getSchemaPath(schema, schema.properties.a.properties.b);
        expect(result).toEqual(['a', 'b']);
    });
    test('Nested property in second branch', () => {
        const schema = {
            properties: {
                a: { properties: { ab: {} } },
                b: { properties: { bb: {} } }
            }
        };
        const result = getSchemaPath(schema, schema.properties.b.properties.bb);
        expect(result).toEqual(['b', 'bb']);
    });
});

describe('getSubSchema', () => {
    test('Empty if no properties', () => {
        const result = getSubSchema({}, 'a.b');
        expect(result).toEqual({});
    });
    test('Empty if no path', () => {
        const result = getSubSchema(
            { properties: { a: { properties: { b: {} } } } },
            ''
        );
        expect(result).toEqual({});
    });
    test('Empty if no match', () => {
        const result = getSubSchema(
            { properties: { a: { properties: { b: {} } } } },
            'a.c'
        );
        expect(result).toEqual({});
    });
    test('Single property', () => {
        const schema = { properties: { a: { blah: 'blah' } } };
        const result = getSubSchema(schema, 'a');
        expect(result).toEqual(schema.properties.a);
    });
    test('Nested property', () => {
        const schema = {
            title: 'blah',
            properties: { a: { properties: { b: { blah: 'blah' } } } }
        };
        const result = getSubSchema(schema, 'a.b');
        expect(result).toEqual(schema.properties.a.properties.b);
    });
});
