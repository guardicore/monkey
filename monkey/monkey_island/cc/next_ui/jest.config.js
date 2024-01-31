/**
 * For a detailed explanation regarding each configuration property, visit:
 * https://jestjs.io/docs/configuration
 */

/** @type {import('jest').Config} */
const config = {
    clearMocks: true,
    collectCoverage: true,
    coverageDirectory: 'coverage',
    coverageProvider: 'v8',
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/src/$1'
    },
    roots: ['<rootDir>/src'],
    slowTestThreshold: 5,
    testEnvironment: 'jsdom',
    transform: {
        '.+\\.(j|t)sx?$': '@swc/jest'
    }
};

// eslint-disable-next-line no-undef
module.exports = config;
