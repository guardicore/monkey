import React from 'react';
import LogoutButton from './LogoutButton';

describe('LogoutButton', () => {
    it('renders', () => {
        // see: https://on.cypress.io/mounting-react
        cy.mount(<LogoutButton />);
    });
});
