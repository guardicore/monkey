import { mount } from 'cypress/react18';
import { ReduxProvider } from '@/providers/reduxProvider/provider';

Cypress.Commands.add('mount', (component, options) => {
    // Wrap any parent components needed
    const wrapped = <ReduxProvider>{component}</ReduxProvider>;
    return mount(wrapped, options);
});
