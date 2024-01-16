/**
 * For a detailed explanation regarding each configuration property, visit:
 * https://jestjs.io/docs/configuration
 */

import type { Config } from 'jest';

const config: Config = {
    // All imported modules in your tests should be mocked automatically
    // automock: false,

    // Automatically clear mock calls, instances, contexts and results before every test
    clearMocks: true,

    // Indicates whether the coverage information should be collected while executing the test
    collectCoverage: true,

    // The directory where Jest should output its coverage files
    coverageDirectory: 'coverage',

    // An array of regexp pattern strings used to skip coverage collection
    // coveragePathIgnorePatterns: [
    //   "/node_modules/"
    // ],

    // Indicates which provider should be used to instrument code for coverage
    coverageProvider: 'v8',

    // An object that configures minimum threshold enforcement for coverage results
    // coverageThreshold: undefined,

    // Activates notifications for test results
    // notify: false,

    // An enum that specifies notification mode. Requires { notify: true }
    // notifyMode: "failure-change",

    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/src/$1'
    },

    // A preset that is used as a base for Jest's configuration
    preset: 'ts-jest',

    // A list of paths to directories that Jest should use to search for files in
    roots: ['<rootDir>/src'],

    // The number of seconds after which a test is considered as slow and reported as such in the results.
    // slowTestThreshold: 5,

    // The test environment that will be used for testing
    testEnvironment: 'jsdom',

    // Options that will be passed to the testEnvironment
    // testEnvironmentOptions: {},

    // A map from regular expressions to paths to transformers
    transform: {
        '.+\\.(j|t)sx?$': 'ts-jest'
    }
};

export default config;
