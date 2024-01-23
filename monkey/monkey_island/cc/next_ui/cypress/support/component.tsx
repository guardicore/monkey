import { mount } from 'cypress/react18';
import { ReduxProvider } from '@/providers/reduxProvider/provider';

// Currently, Cypress does not support importing CSS files with Next.js 13+
// in component tests.
// See: https://github.com/cypress-io/cypress/issues/27890
// import '@/styles/globals.scss';

Cypress.Commands.add('mount', (component, options) => {
    // Wrap any parent components needed
    const wrapped = <ReduxProvider>{component}</ReduxProvider>;
    return mount(wrapped, options);
});
