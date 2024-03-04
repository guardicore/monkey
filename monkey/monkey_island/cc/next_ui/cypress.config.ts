import { defineConfig } from 'cypress';

export default defineConfig({
    component: {
        supportFile: 'cypress/support/component.tsx',
        devServer: {
            framework: 'next',
            bundler: 'webpack'
        }
    },

    e2e: {
        baseUrl: 'https://localhost:8443',
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        setupNodeEvents(on, config) {
            // implement node event listeners here
        }
    }
});
